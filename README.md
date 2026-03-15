# UT JSON Workspace

Folder ini berisi skrip untuk mengekstrak teks buku Kotobee menjadi file JSON.

## File yang sebaiknya masuk repo

- `extract_kotobee.py`
- `clean_json.py`
- `Mulai_Ekstrak_Buku.bat`
- `.gitignore`
- `README.md`

## File yang sebaiknya tidak masuk repo

- `antigravity_chrome_profile/`
- `UT_Book_*.json`
- `node_modules/`
- `playwright-report/`
- `test-results/`
- `blob-report/`
- `.cache/`

Alasannya sederhana: file-folder itu adalah hasil generate, cache, atau data lokal yang bisa membuat repo menjadi berat.

## Langkah paling aman untuk pemula

1. Pasang Git atau GitHub Desktop terlebih dahulu.
2. Pastikan folder ini sudah punya file `.gitignore`.
3. Upload file kode lebih dulu, jangan upload seluruh isi folder secara mentah.
4. Setelah berhasil, baru putuskan apakah ada file output JSON yang memang ingin disimpan di repo.

## Jika memakai Git di terminal

Jalankan perintah berikut dari folder ini:

```powershell
git init
git add extract_kotobee.py clean_json.py Mulai_Ekstrak_Buku.bat .gitignore README.md
git commit -m "Initial import"
git branch -M main
git remote add origin URL_REPO_GITHUB_KAMU
git push -u origin main
```

Ganti `URL_REPO_GITHUB_KAMU` dengan URL repo GitHub milikmu.

## Jika memakai GitHub Desktop

1. Buka GitHub Desktop.
2. Pilih `Add an Existing Repository from your Hard Drive`.
3. Arahkan ke folder ini.
4. Publish repository ke GitHub.
5. Pastikan file besar seperti `antigravity_chrome_profile` tidak ikut terpilih.

## Rekomendasi untuk folder ini

Untuk kondisi folder saat ini, yang paling aman adalah:

- pindahkan file skrip Python dan file `.bat`
- jangan masukkan `antigravity_chrome_profile` karena ukurannya besar dan isinya profil browser
- jangan masukkan `UT_Book_*.json` kecuali memang ingin menyimpan contoh output
