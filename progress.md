# Progres

- Fondasi baseline diimpor ke repository baru, checkpoint 127cb05.
- Repository GitHub baru dibuat. Implementasi V6, build, preview dari BIN, dan 27 test selesai.
- Preview diperiksa visual; raster digit diperbaiki supaya posisi sel stabil, warna solid, dan jarak antar digit 2 px.
- README, catatan implementasi, requirements, preview interaktif, dan checklist perangkat selesai.
- Kode, BIN, preview, dan dokumentasi sudah di-push ke GitHub.
- Audit remote membandingkan kedua BIN dan preview normal/AOD dengan file lokal. Bukti disimpan di `out/remote-verification.json`.
- Sisa penerimaan: uji perangkat oleh pengguna, sesuai `docs/device-test.md`.

- Revisi digit 1: lebar tinta 61 menjadi 45 px pada jam dan menit. Regresi berhasil direproduksi sebelum perbaikan, kemudian 27 test lulus dan preview diperiksa ulang.

- 14 September: warna menit disamakan dengan abu-abu muda simbol U (#848688), normal dan AOD. Preview dari BIN diperbarui; 27 test lulus.

- 16 September: optimasi aset AOD mempertahankan semua komponen. Normal tidak berubah, 30 test lulus, laporan sembilan waktu dan perbandingan AOD tersedia. Uji baterai fisik pending.

- Angka tanggal diperbesar menjadi 17 px pada normal/AOD; seluruh kombinasi tanggal diperiksa ulang.
