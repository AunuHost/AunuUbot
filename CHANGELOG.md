# Changelog

## 2026-10-26 — Fix KeyError & formatting crash yt_dl (missing import USER_GROUP & mixed bracket syntax). Fix base64 padding calculation di unpackInlineMessage dan AttributeError NoneType pada member list_admins di tools.py. Tangkap exception send_message startup ke OWNER_ID agar bot tidak crash saat owner belum start bot.

- `AunuUbot/core/helpers/yt_dl.py`
- `AunuUbot/core/helpers/tools.py`
- `AunuUbot/core/function/plugins.py`

## 2026-10-25 — Ditemukan bug nyata di `__init__.py`: event loop handling deprecated di Python 3.10+. Juga ada bug di `__main__.py` yang menghapus semua session file (`rm -rf *session*`) yang bisa menghapus file penting. Bug paling kritis: di `core/helpers/tools.py` fungsi `unpackInlineMessage` salah mengkonversi chat_id — string replace `-1` ke `-1001` bisa salah jika chat_id tidak dimulai dengan `-1`. Dan di `core/function/expired.py`, perbandingan `now.date() >= exp_date.date()` berarti userbot dihapus PADA hari expired, bukan setelahnya — ini mungkin disengaja tapi bisa menyebabkan penghapusan prematur (user kehilangan akses di hari terakhir). Bug paling nyata dan berbahaya: `bash("rm -rf *session*")` di __main__.py bisa menghapus file yang cocok pattern glob `*session*` di current working directory. Ini seharusnya hanya menghapus file .session pyrogram. Fix: buat pattern lebih spesifik. Juga `BLACKLIST_CHAT` di config.py akan crash jika env var kosong string karena `int('')` akan raise ValueError.

- `AunuUbot/config.py`
- `AunuUbot/__main__.py`
- `AunuUbot/__init__.py`

## 2026-10-21 — Implementasi fitur 'prefix clone' — saat userbot membalas/mention seseorang, profil (nama, bio, foto profil) target di-copy ke akun userbot. Ada command `.prefixclone` (atau `.pclone`) untuk aktifkan mode, dan `.unprefixclone` (atau `.unpclone`) untuk revert ke profil asli. Backup profil asli disimpan di DB (vars_store). File yang diubah: modules/prefix_tools.py (implementasi utama) dan core/database/__init__.py (tambah tabel backup profil).

- `AunuUbot/modules/prefix_tools.py`

## 2026-10-21 — Bug kritis: `get_pref` dipanggil di `Ubot.start()` sebelum diimpor (import ada di bawah file). Ini menyebabkan NameError saat runtime. Fix: pindahkan pemanggilan `get_pref` agar menggunakan late-binding import, atau restruktur import. Solusi paling aman: gunakan lazy import di dalam method `start()`.

- `AunuUbot/__init__.py`

