# Perbaikan layout v5, 12 September 2026

Preview sebelumnya menumpuk karena latar referensi ditambal sebagian,
sementara cincin, ikon, dan angka baru memakai koordinat yang berbeda.
Area langkah masuk ke jam, ikon hati berada di luar cincinnya, dan ikon
matahari menyentuh angkanya. Raster SVG berlatar putih juga ikut diberi
warna merah sehingga ikon hati dan api menjadi kotak.

Latar sekarang dibangun dari kanvas hitam dengan cincin dan aksen vektor.
Hanya ilustrasi kampus di bagian bawah yang diambil dari referensi.
Empat cincin diberi ruang terpisah dari jam, dan posisi nilai dihitung
agar angka maksimum tetap muat. Mask tinta SVG diambil sebelum diberi
warna. Titik dua always-on mengikuti posisi vertikal jamnya.

## Verifikasi

- `python tools/build_all.py`: lulus. Lima preview dirender dari hasil
  ekstraksi file `.bin`, termasuk harian, maksimum, nol, sunrise, dan idle.
- `python -m unittest discover -s tools -p "test_*.py"`: 17 test lulus.
- `tools/check_layout.py` menolak 11 pasangan elemen bertabrakan pada BIN
  checkpoint `26694a3`. Layout baru memiliki 0 tabrakan, baik pada aset
  sumber maupun pada hasil ekstraksi BIN.
- Pemeriksaan mencakup seluruh varian hari, bulan, banner cuaca, banner
  matahari, AM/PM, digit, posisi suffix pada setiap panjang angka, dan
  sprite tanpa data. Angka metrik harus berada di dalam cincin.
- Test dengan posisi denyut sengaja dipindah ke area menit membuktikan
  bahwa validator menolak tabrakan baru.
- Pemeriksaan layar bulat lulus. Parameter dan piksel sumber identik
  dengan hasil ekstraksi BIN, dengan selisih piksel maksimum 0.
- Lima preview diperiksa secara visual. File instalasi utama dan alias
  `telu_university_v5.bin` dibangun ulang bersama preview di dalam paket.

Ukuran dan SHA-256 artefak ada di `out/validation.json`. Hasil di atas
adalah validasi build dan simulasi. V5 yang diperbaiki masih memerlukan
uji di perangkat; laporan v4 berjalan di jam tidak dianggap sebagai
hasil uji perangkat untuk v5.

## Riwayat kerja

Perubahan v5 yang sudah ada disimpan sebagai checkpoint lokal sebelum
perbaikan. Perbaikan generator dan penambahan validator disimpan dalam
commit terpisah. Artefak final serta catatan ini disimpan setelah build
dan pengujian lulus, lalu dikirim bersama ke GitHub.
