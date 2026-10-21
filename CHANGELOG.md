# Changelog

## 2026-10-21 — Implementasi fitur 'prefix clone' — saat userbot membalas/mention seseorang, profil (nama, bio, foto profil) target di-copy ke akun userbot. Ada command `.prefixclone` (atau `.pclone`) untuk aktifkan mode, dan `.unprefixclone` (atau `.unpclone`) untuk revert ke profil asli. Backup profil asli disimpan di DB (vars_store). File yang diubah: modules/prefix_tools.py (implementasi utama) dan core/database/__init__.py (tambah tabel backup profil).

- `AunuUbot/modules/prefix_tools.py`

## 2026-10-21 — Bug kritis: `get_pref` dipanggil di `Ubot.start()` sebelum diimpor (import ada di bawah file). Ini menyebabkan NameError saat runtime. Fix: pindahkan pemanggilan `get_pref` agar menggunakan late-binding import, atau restruktur import. Solusi paling aman: gunakan lazy import di dalam method `start()`.

- `AunuUbot/__init__.py`

