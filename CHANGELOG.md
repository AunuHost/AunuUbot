# Changelog

## 2026-10-21 — Bug kritis: `get_pref` dipanggil di `Ubot.start()` sebelum diimpor (import ada di bawah file). Ini menyebabkan NameError saat runtime. Fix: pindahkan pemanggilan `get_pref` agar menggunakan late-binding import, atau restruktur import. Solusi paling aman: gunakan lazy import di dalam method `start()`.

- `AunuUbot/__init__.py`

