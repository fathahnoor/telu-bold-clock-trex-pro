# Temuan

- Baseline: fathahnoor/telu-amazfit-trex-pro-watchface, commit c7a48cc81ba5a4607fd49bd92c742447765be021.
- Format: UIHH v2, device ID 83, blok QuickLZ 4096 byte, gambar BGRA, referensi gambar firmware mulai 1.
- Pertahankan packer dan codec. Jangan memakai Alignment Right.
- Solar memakai Type Sunrise (12), NumberSequence tanpa subtype dan dua banner Linear. Transisi persis terhadap sunrise/sunset belum terbukti di firmware.
- Renderer baseline melewatkan minus suhu. Catatan format baseline menyediakan DelimiterImageIndex untuk minus Weather; perlu adaptasi renderer dan validator agar preview jujur.
- Pillow, svglib, dan reportlab tersedia tanpa instalasi tambahan.
- V6: 150 gambar termasuk preview internal, 491755 byte, piksel round-trip delta 0.
- 30 unit test lulus. Sembilan waktu stress dan enam skenario wajib sudah dirender dari BIN.
- Codec dan packer memiliki SHA-256 identik dengan baseline; audit ada di `out/qa.json`.
- Parameter suhu negatif ditambahkan sesuai catatan format baseline. Renderer dan validator sudah menguji minus; firmware tetap perlu diperiksa.

- Koreksi pengguna: digit 1 terlalu lebar akibat fit_width. Kini digit 1 memakai proporsi alami, tinta 45 px di tengah sel 61 px.

- Warna menit mengikuti revisi pengguna 14 September: #848688, RGB (132,134,136), diambil dari warna isi abu-abu muda aset logo Tel-U.

- AOD: LUT saat build, 20 sprite tambahan, metrik/tanggal berbagi aset. Tidak ada kontrol refresh tervalidasi. Laporan RGB bukan pengukuran daya.
