# UT JSON Extractor

Konversi buku UT berbasis Kotobee menjadi file JSON, lalu bersihkan hasil ekstraksinya agar lebih rapi dan siap dipakai untuk pencarian, analisis, atau pipeline AI/RAG.

> Repo ini difokuskan pada skrip inti. File hasil ekstraksi, cache browser, dan profil Playwright sengaja tidak ikut dipublikasikan agar repository tetap ringan dan rapi.

## Ringkasan

Project ini memiliki dua langkah utama:

1. Mengekstrak isi buku yang sedang terbuka di reader Kotobee menggunakan Playwright.
2. Membersihkan teks hasil ekstraksi dari elemen UI yang tidak relevan, seperti tombol navigasi, menu, dan teks duplikat.

Hasil akhirnya adalah file JSON yang lebih bersih dan lebih mudah diproses lebih lanjut.

## Fitur

- Mendeteksi tab reader Kotobee yang sedang aktif secara otomatis.
- Mengambil teks dari halaman utama, `iframe`, dan elemen `svg`.
- Melanjutkan ekstraksi halaman demi halaman sampai halaman terakhir terdeteksi.
- Menyimpan hasil ekstraksi ke file JSON dengan nama unik berbasis waktu.
- Membersihkan teks sampah dari antarmuka reader.
- Menghapus halaman atau potongan teks yang terduplikasi.
- Menghasilkan file akhir `_clean.json` yang lebih siap dipakai untuk AI atau RAG.

## Struktur Project

| File | Fungsi |
| --- | --- |
| `extract_kotobee.py` | Skrip utama untuk membuka sesi browser dan mengekstrak isi buku ke JSON |
| `clean_json.py` | Membersihkan hasil JSON dari noise UI dan duplikasi |
| `Mulai_Ekstrak_Buku.bat` | Shortcut Windows untuk menjalankan proses ekstraksi |
| `.gitignore` | Mencegah file hasil generate, cache, dan profil lokal ikut masuk repo |
| `antigravity_chrome_profile/` | Profil browser lokal untuk sesi Playwright, tidak untuk dipublikasikan |
| `UT_Book_*.json` | File output hasil ekstraksi, tidak ikut dilacak Git secara default |

## Cara Kerja

1. Jalankan skrip ekstraksi.
2. Browser Chrome akan terbuka memakai profil lokal.
3. Login ke platform UT jika diperlukan.
4. Buka buku sampai tampilan reader benar-benar muncul.
5. Skrip akan mendeteksi tab yang sesuai dan mulai mengekstrak isi halaman satu per satu.
6. Setelah selesai, hasil disimpan ke file `UT_Book_YYYYMMDD_HHMMSS.json`.
7. Jalankan skrip pembersih untuk menghasilkan versi `*_clean.json`.

## Kebutuhan

- Windows
- Python 3
- Google Chrome
- Paket Python `playwright`

## Instalasi

Install dependency Python:

```bash
pip install playwright
```

Jika environment Playwright kamu belum siap, jalankan juga:

```bash
playwright install
```

## Menjalankan Ekstraksi

Cara termudah di Windows:

```bat
Mulai_Ekstrak_Buku.bat
```

Atau langsung lewat Python:

```bash
python extract_kotobee.py
```

Setelah browser terbuka:

1. Login bila diminta.
2. Buka buku UT sampai reader aktif.
3. Biarkan skrip bekerja otomatis.

Output akan tersimpan dalam format seperti ini:

```text
UT_Book_20260315_125731.json
```

## Membersihkan Hasil JSON

Untuk membersihkan satu file:

```bash
python clean_json.py UT_Book_20260315_125731.json
```

Untuk membersihkan semua file hasil ekstraksi di folder:

```bash
python clean_json.py
```

Output bersih akan disimpan dengan suffix berikut:

```text
UT_Book_20260315_125731_clean.json
```

## Format Output

Contoh struktur hasil ekstraksi:

```json
{
  "url_source": "https://contoh-reader",
  "extraction_time": "20260315_125731",
  "total_pages": 120,
  "data": [
    {
      "page": 1,
      "text": "Isi halaman..."
    }
  ]
}
```

## Catatan Penting

- Folder `antigravity_chrome_profile/` berisi data sesi lokal, cache, history, dan data browser lain. Folder ini tidak cocok untuk dipublikasikan ke GitHub.
- File `UT_Book_*.json` adalah hasil generate. Secara default file ini tidak ikut masuk Git agar repo tetap ringan.
- Skrip ini bergantung pada tampilan reader yang aktif. Jika struktur halaman UT berubah, selector mungkin perlu diperbarui.
- Beberapa halaman dapat terdeteksi kosong bila isinya berupa gambar, video, atau elemen yang tidak memiliki teks yang bisa diambil.

## Untuk Publikasi Repo

Agar repo tetap bersih dan nyaman dipakai orang lain, yang sebaiknya dipublikasikan adalah:

- skrip Python
- file batch
- `.gitignore`
- dokumentasi

Yang sebaiknya tetap lokal:

- profil browser Playwright
- cache
- report hasil testing
- file output JSON besar, kecuali memang ingin dijadikan contoh

## Cocok Untuk

- ekstraksi konten buku UT
- pembersihan teks hasil reader digital
- persiapan dataset untuk indexing
- bahan awal untuk chatbot, semantic search, atau RAG

## Disclaimer

Gunakan project ini dengan bijak dan pastikan pemakaian konten mengikuti hak akses serta kebijakan platform yang berlaku.
