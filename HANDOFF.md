# Status TEL-U Performance V6

Untuk build ulang: `python tools/build_all.py`, lalu `python -m unittest discover -s tools -p "test_*.py"` setelah build berhasil.

Implementasi dan validasi software selesai. BIN: `out/telu_university_v6.bin`, 491755 byte, SHA-256 `04bd8391e07bcc9c7c9a5143a4241149e3b3cd6a2e21ba2db3ccf40c8bcbcc0d`.
30 unit test lulus. Normal sama dengan rilis sebelumnya; AOD lebih redup dengan komponen dan posisi sama. `out/qa.json` adalah snapshot audit penyerahan; `out/validation.json` dihasilkan ulang saat build.

Sumber visual: `V6-REF.png` dan `TELU_WATCHFACE_V6_DESIGN_SPEC.md` di root.
Sumber teknis beserta commit ada di `findings.md`. Repository lama tidak diubah.
Repo tujuan: https://github.com/fathahnoor/telu-bold-clock-trex-pro.
Branch `main` sudah di-push. Snapshot pemeriksaan file remote ada di `out/remote-verification.json`.
Pengguna sudah mengizinkan build, commit, pembuatan repo, dan push.
Physical device test pending. Solar memakai mekanisme closest-event firmware baseline; tiga transisi target belum dibuktikan. Konsumsi AOD dan pemetaan cuaca juga belum diukur di perangkat.
Detail tahapan ada di `task_plan.md`, checklist fisik di `docs/device-test.md`.

Revisi proporsi digit 1: tinta 45 px dalam sel 61 px, tinggi 88 px. Preview normal/AOD dan stress sudah dibangun ulang; 27 test lulus.

Revisi 14 September: digit menit #848688, sama dengan abu-abu muda pada simbol U logo. Build dan 27 test lulus.

16 September: optimasi AOD selesai, lihat docs/aod-power.md dan out/aod-analysis.json. Penghematan baterai belum diukur. Paket pembanding ada di out/baseline/.
