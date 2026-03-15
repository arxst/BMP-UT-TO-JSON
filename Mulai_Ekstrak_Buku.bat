@echo off
title Kotobee Auto Extractor by Antigravity
color 0A

echo ==============================================================
echo       KOTOBEE AUTO EXTRACTOR UT - POWERED BY ANTIGRAVITY
echo ==============================================================
echo.
echo Selamat datang! 
echo Script ini akan secara otomatis membuka browser dan alat ekstraktor.
echo.
echo PEMBERITAHUAN PENTING:
echo Jika saat ini ekstraksi sedang berjalan (Terminal yang lama masih jalan),
echo biarkan saja sampai selesai. Anda baru boleh menekan tombol di bawah ini
echo untuk mengekstrak buku baru.
echo.
pause

echo.
echo [*] Menjalankan script Python...
python extract_kotobee.py

echo.
echo [*] Eksekusi Selesai.
pause
