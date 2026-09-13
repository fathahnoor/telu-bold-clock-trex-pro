# Status TEL-U Performance V6

Untuk build ulang: `python tools/build_all.py`, lalu `python -m unittest discover -s tools -p "test_*.py"` setelah build berhasil.

Implementasi dan validasi software selesai. BIN: `out/telu_university_v6.bin`, 428.237 byte, SHA-256 `d97cbb51b76ddf8cfa493776461f0945d804084acbb100b6d53a77b3767150dc`.
27 unit test lulus. Preview berasal dari ekstraksi BIN, normal dan AOD identik per piksel. `out/qa.json` adalah snapshot audit penyerahan; `out/validation.json` dihasilkan ulang saat build.

Sumber visual: `V6-REF.png` dan `TELU_WATCHFACE_V6_DESIGN_SPEC.md` di root.
Sumber teknis beserta commit ada di `findings.md`. Repository lama tidak diubah.
Repo tujuan: https://github.com/fathahnoor/telu-bold-clock-trex-pro.
Branch `main` sudah di-push. Snapshot pemeriksaan file remote ada di `out/remote-verification.json`.
Pengguna sudah mengizinkan build, commit, pembuatan repo, dan push.
Physical device test pending. Solar memakai mekanisme closest-event firmware baseline; tiga transisi target belum dibuktikan. Konsumsi AOD dan pemetaan cuaca juga belum diukur di perangkat.
Detail tahapan ada di `task_plan.md`, checklist fisik di `docs/device-test.md`.

Revisi proporsi digit 1: tinta 45 px dalam sel 61 px, tinggi 88 px. Preview normal/AOD dan stress sudah dibangun ulang; 27 test lulus.
