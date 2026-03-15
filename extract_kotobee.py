import asyncio
import json
import time
from playwright.async_api import async_playwright

USER_DATA_DIR = "./antigravity_chrome_profile"

JS_EXTRACT = '''() => {
    const allText = [];
    const extractFromWindow = (win) => {
        try {
            if (win.document && win.document.body) {
                const bodyText = win.document.body.innerText.trim();
                if (bodyText) allText.push(bodyText);
            }
            const svgs = win.document.querySelectorAll('svg');
            svgs.forEach(svg => {
                const svgText = svg.textContent.trim();
                if (svgText) allText.push(svgText);
            });

            const iframes = win.document.querySelectorAll('iframe');
            iframes.forEach(f => {
                if (f.contentWindow) extractFromWindow(f.contentWindow);
            });
        } catch (e) {}
    };
    
    extractFromWindow(window);
    return allText.join('\\n\\n').trim();
}'''

JS_CLICK_NEXT = '''() => {
    const nextBtn = document.querySelector('a.next.chapterBtn') || 
                    document.querySelector('.icon-right-open') || 
                    document.querySelector('.next-btn');
                    
    if (nextBtn && !nextBtn.classList.contains('disabled') && nextBtn.style.display !== 'none') {
        nextBtn.click();
        return true;
    }
    return false;
}'''

async def extract_book(page):
    extracted = []
    page_num = 1
    prev_content = ""
    duplicate_count = 0
    
    # Tunggu sebentar untuk render iframe awal
    print("[*] Menunggu iframe reader terbuka sempurna (10 detik)...")
    await page.wait_for_timeout(10000)
    
    while True:
        print(f"[*] Mengekstrak Teks Halaman {page_num}...")
        
        # Catat URL sebelum klik Next (untuk deteksi halaman terakhir)
        url_before = page.url
        
        # Polling berulang-ulang sampai teks muncul (max 20 detik)
        content = ""
        for i in range(10):
            try:
                content = await page.evaluate(JS_EXTRACT)
                if content and len(content) > 50:
                    break
            except Exception as e:
                pass
            await page.wait_for_timeout(2000)
            
        if not content or len(content) <= 50:
            print(f"  [!] Teks kosong di Halaman {page_num} (mungkin sampul/gambar/video).")
            content = "[GAMBAR/VIDEO/HALAMAN KOSONG]"
        else:
            print(f"  [+] Berhasil! Dapat {len(content)} karakter teks.")
        
        # === DETEKSI DUPLIKAT (halaman terakhir) ===
        if content == prev_content and content != "[GAMBAR/VIDEO/HALAMAN KOSONG]":
            duplicate_count += 1
            if duplicate_count >= 2:
                print(f"  [!] Teks sama persis dengan halaman sebelumnya ({duplicate_count}x).")
                print("[*] Terdeteksi sudah di HALAMAN TERAKHIR. EKSTRAKSI SELESAI!")
                break
        else:
            duplicate_count = 0
            
        prev_content = content
            
        extracted.append({
            "page": page_num,
            "text": content
        })
        
        # Klik Next
        try:
            clicked = await page.evaluate(JS_CLICK_NEXT)
            if not clicked:
                print(f"[*] Tombol NEXT tidak ditemukan atau tidak aktif di Halaman {page_num}.")
                print("[*] EKSTRAKSI SELESAI!")
                break
        except Exception as e:
            print(f"[!] Error saat klik NEXT: {e}")
            break
            
        # Tunggu sedikit sebelum baca halaman berikutnya
        await page.wait_for_timeout(3000)
        
        # === DETEKSI URL TIDAK BERUBAH (halaman terakhir) ===
        url_after = page.url
        if url_after == url_before:
            print(f"  [!] URL tidak berubah setelah klik Next (masih: {url_after}).")
            print("[*] Terdeteksi sudah di HALAMAN TERAKHIR. EKSTRAKSI SELESAI!")
            break
            
        page_num += 1
        
    return extracted

async def main():
    print("[*] Menjalankan Playwright mode SUPER AMAN...")
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            channel="chrome",
            viewport={"width": 1280, "height": 800}
        )
        
        print("\n============================================================")
        print("PERHATIAN: Buka tab browser yang baru saja muncul.")
        print("1. Pastikan Anda sudah login.")
        print("2. Buka BUKU APAPUN yang ingin diekstrak SAMPAI HALAMAN BACA TERBUKA.")
        print("3. BACA INI PENTING: Jangan tekan Enter apa-apa di sini.")
        print("   Script ini akan MENDETEKSI TERUS MENERUS layar browser Anda secara otomatis,")
        print("   dan baru bekerja jika ada buku yang terbuka di URL tab!")
        print("============================================================\n")
        
        target_page = None
        has_iframe = False
        while True:
            for page in browser.pages:
                url = page.url.lower()
                # Cek jika URL adalah reader dari Kotobee
                if "reader/chapter" in url or "book" in url:
                    try:
                        frames_count = await page.evaluate("document.querySelectorAll('iframe').length")
                        if frames_count > 0:
                            target_page = page
                            has_iframe = True
                            break
                    except:
                        pass
            
            if has_iframe and target_page:
                break
                
            await asyncio.sleep(3) # Polling tiap 3 detik
            
        # Bikin nama file output unik berdasarkan waktu saat ini
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"UT_Book_{timestamp}.json"
        
        print(f"\\n[*] BINGO! Tab reader TERKUNCI: {target_page.url}")
        print(f"[*] Hasil akan otomatis disimpan ke file bernama: {output_file}")
        
        # Mulai tarik data
        data = await extract_book(target_page)
        
        print("\n[*] MENYIMPAN HASIL...")
        if data:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "url_source": target_page.url,
                    "extraction_time": timestamp,
                    "total_pages": len(data),
                    "data": data
                }, f, ensure_ascii=False, indent=4)
            print(f"[+] 100% SUKSES! File tersimpan: {output_file}")
        else:
            print("[-] Gagal mengekstrak teks apapun.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
