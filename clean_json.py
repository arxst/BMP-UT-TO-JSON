"""
Script Pembersih JSON Kotobee
Menghapus semua teks "sampah" UI dari hasil ekstraksi buku Kotobee.
Penggunaan: python clean_json.py <nama_file.json>
Atau: python clean_json.py  (akan memproses semua file UT_Book_*.json)
"""
import json
import sys
import glob
import re

# Daftar teks UI Kotobee yang PASTI sampah dan harus dihapus
JUNK_EXACT_LINES = {
    "Library", "Next", "Previous", "Chapters", "Media", "Notebook",
    "Search", "Settings", "View Profile", "Use styling",
    "Auto-adjust line height", "Toggle fullscreen view",
    "Page view", "Auto", "Single page", "Double page", "Scroll",
    "Page animation", "Page flip", "Hardcover flip", "Card-flip",
    "Slide", "Stack", "Fade", "Interface language",
    # Bahasa-bahasa di settings
    "English", "Français", "Español", "Português", "Nederlands",
    "Deutsch", "Magyar", "Italiano", "Svenska", "Melayu",
    "Norsk", "Polski", "Român", "Pусский", "Türkçe", "Cymraeg",
    "Ελληνικά", "العربية", "汉语", "漢語", "日本語", "한국어",
    # Navigasi
    "Next ", " Previous",
}

# Pola regex untuk mendeteksi sampah
JUNK_PATTERNS = [
    r"^Table of Contents$",
    r"^MODUL \d+$",
    r"^Halaman [\d\.\s]+$",
    r"^\d+@ecampus\.ut\.ac\.id$",
    r"^[A-Z\s]{5,}$",  # nama user uppercase penuh (ARIZAL SHAKTIANTORO)
]

# Teks yang mengandung substring ini => hapus baris itu
JUNK_SUBSTRINGS = [
    "@ecampus.ut.ac.id",
    "View Profile",
    "Use styling",
    "Auto-adjust line height",
    "Toggle fullscreen view",
    "Interface language",
]

def is_junk_line(line: str) -> bool:
    """Cek apakah satu baris adalah sampah UI."""
    stripped = line.strip()
    
    if not stripped:
        return False  # baris kosong biarkan dulu, nanti dirapikan
    
    # Exact match
    if stripped in JUNK_EXACT_LINES:
        return True
    
    # Substring match
    for sub in JUNK_SUBSTRINGS:
        if sub in stripped:
            return True
    
    # Regex match
    for pattern in JUNK_PATTERNS:
        if re.match(pattern, stripped):
            return True
    
    return False

def clean_page_text(raw_text: str) -> str:
    """Bersihkan teks satu halaman dari sampah UI Kotobee."""
    lines = raw_text.split("\n")
    clean_lines = []
    
    for line in lines:
        if not is_junk_line(line):
            clean_lines.append(line)
    
    # Gabungkan kembali
    result = "\n".join(clean_lines)
    
    # Hapus blok navigasi yang sering muncul berurutan
    # Contoh: "Next \n Previous\nChapters\nMedia..."
    nav_block_pattern = r"(Next\s*\n\s*Previous|Previous\s*\n\s*Next)"
    result = re.sub(nav_block_pattern, "", result)
    
    # Hapus baris kosong berlebihan (lebih dari 2 berturut-turut)
    result = re.sub(r"\n{3,}", "\n\n", result)
    
    return result.strip()

def remove_duplicate_content(pages: list) -> list:
    """Hapus konten duplikat antar halaman berurutan."""
    cleaned = []
    prev_text = ""
    
    for page in pages:
        text = page["text"]
        
        # Jika teks ini persis sama dengan halaman sebelumnya, skip
        if text == prev_text:
            continue
        
        # Jika teks halaman sebelumnya muncul lagi di halaman ini (karena iframe ganda),
        # hapus bagian duplikat
        if prev_text and len(prev_text) > 100:
            # Cari apakah teks halaman sebelumnya ada di halaman ini
            if prev_text in text:
                text = text.replace(prev_text, "").strip()
        
        if text and len(text) > 10:  # Abaikan halaman yang terlalu pendek setelah dibersihkan
            cleaned.append({
                "page": len(cleaned) + 1,  # Re-number
                "text": text
            })
            prev_text = text
    
    return cleaned

def process_file(filepath: str):
    """Proses satu file JSON."""
    print(f"\n[*] Membersihkan: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_pages = len(data.get("data", []))
    original_size = sum(len(p["text"]) for p in data.get("data", []))
    
    # Step 1: Bersihkan tiap halaman dari sampah UI
    for page in data["data"]:
        page["text"] = clean_page_text(page["text"])
    
    # Step 2: Hapus halaman duplikat/kosong
    data["data"] = remove_duplicate_content(data["data"])
    data["total_pages"] = len(data["data"])
    
    clean_size = sum(len(p["text"]) for p in data["data"])
    
    # Simpan dengan suffix _clean
    output_path = filepath.replace(".json", "_clean.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    reduction = ((original_size - clean_size) / original_size * 100) if original_size > 0 else 0
    
    print(f"  [+] Halaman: {original_pages} -> {data['total_pages']}")
    print(f"  [+] Ukuran teks: {original_size:,} -> {clean_size:,} karakter ({reduction:.1f}% lebih kecil)")
    print(f"  [+] Tersimpan: {output_path}")
    
    return output_path

def main():
    if len(sys.argv) > 1:
        # Proses file yang diberikan
        files = sys.argv[1:]
    else:
        # Proses semua file UT_Book_*.json (tapi bukan yang _clean)
        files = [f for f in glob.glob("UT_Book_*.json") if "_clean" not in f]
        # Tambahkan juga file book_*_extracted.json
        files += [f for f in glob.glob("book_*_extracted.json") if "_clean" not in f]
    
    if not files:
        print("[!] Tidak ada file JSON yang ditemukan.")
        print("    Gunakan: python clean_json.py <nama_file.json>")
        print("    Atau pastikan ada file UT_Book_*.json di folder ini.")
        return
    
    print("=" * 60)
    print("   KOTOBEE JSON CLEANER - Pembersih Sampah UI")
    print("=" * 60)
    
    for f in files:
        try:
            process_file(f)
        except Exception as e:
            print(f"  [!] Error memproses {f}: {e}")
    
    print("\n" + "=" * 60)
    print("   SELESAI! File _clean.json siap digunakan untuk AI RAG.")
    print("=" * 60)

if __name__ == "__main__":
    main()
