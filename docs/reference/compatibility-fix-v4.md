# Compatibility v4: warna gambar dan layout terkunci

## Hasil uji pengguna pada v3 (12 September 2026)

Watchface tampil dan aktif di jam. Tiga masalah terlihat dari foto perangkat:

1. Semua elemen merah pada gambar tampil biru: chip "T", kapsul menit, ikon
   KCAL/STEPS/BPM, dan tick merah. Arc baterai yang digambar firmware tetap
   merah. Gambar preview statis (yang memuat kapsul merah) juga tampil biru.
2. Posisi jam meleset: digit jam masuk ke kapsul, digit menit pertama muncul
   di luar kapsul dan sisanya terpotong tepi layar. Teks baterai bergeser.
3. Always-on hanya menampilkan jam bertumpuk dan hari, tanpa metrik lain.

## Akar masalah

**Urutan byte gambar.** Encoder menulis R,G,B,A sementara firmware membaca
B,G,R,A. Pertukaran kanal ini mengubah merah menjadi biru tanpa mengubah
putih dan abu: chip T merah tampil biru, kapsul merah tampil biru, sedangkan
teks putih tetap putih dan arc CircleScale (digambar firmware, bukan gambar)
tetap merah. Preview statis ikut biru karena gambar yang sama diproses jalur
tampilan yang sama.

**Alignment Right tidak dihormati.** Teks NumberSequence dengan Alignment
"Right" digambar firmware mulai dari X dan memanjang ke kanan, bukan berakhir
di X. Jam (X=170) meluber ke dalam kapsul, menit (X=299) keluar layar, dan
baterai (X=220) bergeser ke kanan.

**Idle terpisah.** IdleScreen memakai latar hitam sendiri dan hanya memuat
jam, hari, dan arc baterai.

## Perubahan v4

- `encode_image_32bit` dan `_decode_32bit` menulis dan membaca urutan byte
  B,G,R,A; round-trip piksel tetap eksak (delta 0).
- Semua teks dinamis memakai Alignment Left dengan X eksplisit: jam X=62,
  menit X=191 (zero pad aktif sehingga selalu dua digit), dan angka baterai
  X=159 (muat tiga digit plus suffix persen).
- IdleScreen memakai blok Time, Date, dan Data yang sama persis dengan
  tampilan utama dan background ID 1. AM/PM, tanggal, langkah, kalori,
  denyut, dan angka baterai ikut tampil di always-on.
- `render_mockup.py`, `check_round.py`, dan test regresi diperbarui. Snapshot
  `build/reference_current` disegarkan dari bin v4 mengikuti perilaku parser
  upstream yang menyalin byte piksel apa adanya.
- Test baru: larangan Alignment Right di bin, idle harus sama dengan tampilan
  utama, dan round-trip warna gambar.

## Hasil uji

V4 terpasang dan berjalan di Amazfit T-Rex Pro milik pengguna
(laporan 12 September 2026). Checklist pemasangan untuk pengguna lain:

1. Pastikan merah kembali: chip T, kapsul menit, ikon metrik, dan tick.
2. Pastikan jam putih di kiri kapsul dan menit putih di dalam kapsul.
3. Biarkan layar masuk always-on dan bandingkan dengan tampilan utama;
   semua metrik harus tetap terlihat.
4. Buka daftar watchface: preview harus sama dengan tampilan utama.

Bentuk putih/merah di tepi kiri foto preview kemungkinan UI bawaan jam
(watchface sebelahnya pada carousel), bukan bagian dari aset watchface ini.

Ukuran dan SHA-256 terkini ada pada `out/validation.json`.
