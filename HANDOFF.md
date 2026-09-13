# Status TEL-U Performance V6

Untuk build ulang: `python tools/build_all.py`, lalu `python -m unittest discover -s tools -p "test_*.py"` setelah build berhasil.

Implementasi dan validasi software selesai. BIN: `out/telu_university_v6.bin`, 428.054 byte, SHA-256 `22de5a4a6e89c76b6074eeeaf696a052461269024fb78b318c682d405cf2d083`.
27 unit test lulus. Preview berasal dari ekstraksi BIN, normal dan AOD identik per piksel. `out/qa.json` adalah snapshot audit penyerahan; `out/validation.json` dihasilkan ulang saat build.

Sumber visual: `V6-REF.png` dan `TELU_WATCHFACE_V6_DESIGN_SPEC.md` di root.
Sumber teknis beserta commit ada di `findings.md`. Repository lama tidak diubah.
Repo tujuan: https://github.com/fathahnoor/telu-bold-clock-trex-pro.
Pengguna sudah mengizinkan build, commit, pembuatan repo, dan push.
Physical device test pending. Solar memakai mekanisme closest-event firmware baseline; tiga transisi target belum dibuktikan. Konsumsi AOD dan pemetaan cuaca juga belum diukur di perangkat.
Detail tahapan ada di `task_plan.md`, checklist fisik di `docs/device-test.md`.
