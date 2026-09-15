# Implementasi V6

## Desain dan koordinat

Referensi visual adalah MD dan PNG pengguna di root. Penyesuaian dilakukan untuk digit terbesar, batas lingkaran, dan ruang antarelemen pada raster 360 x 360.

| Elemen | Implementasi |
| --- | --- |
| Jam | X 117, Y 103; dua sel 61 x 88, jarak 2 px, putih |
| Menit | X 117, Y 194; sel yang sama, abu-abu #848688 |
| AM/PM | X 245, Y 160 |
| Hari | X 261, Y 76, merah |
| Tanggal dan bulan | Angka X 259, Y 95, sel 11 x 17; bulan X 285, Y 92 |
| Panel kiri | Steps, BPM, kcal; tanpa CircleScale |
| Panel kanan | Baterai, satu slot solar, cuaca |
| Kampus | X 55, Y 287; 250 x 48, luminansi dibatasi 80/255 |
| AOD | Komponen dan posisi sama; background dan digit waktu memakai versi redup |

Angka Inter Black dipangkas ke tinta sebelum rasterisasi. Sel waktu tetap berukuran 61 x 88 piksel. Digit `1` mempertahankan proporsi alaminya dengan tinta selebar 45 piksel, terpusat di dalam sel dengan margin 8 piksel pada tiap sisi. Digit lain tetap memakai raster sebelumnya. Posisi sel tidak bergeser saat waktu berubah; lebar tinta pasangan dapat berbeda secara alami. Alpha menjadi mask warna solid untuk menjaga putih dan abu-abu dari perubahan RGB pada tepi antialias. Panel memakai kurva dari titik kontrol; teks dan ikon tetap terpisah dari garis panel.

## Batas kompatibilitas

Baseline commit: `c7a48cc81ba5a4607fd49bd92c742447765be021`. Tidak ada reverse engineering baru pada container, codec, kompresi, maupun skema. `trexpro_wf.py` dan `pack_watchface.py` dipakai utuh.

Solar mempertahankan `Type: Sunrise` (12), `NumberSequence` tanpa subtype, titik dua melalui `DecimalPointImageIndex`, dan satu pasangan banner `Linear`. Watchface legacy ini tidak menjalankan Python atau JavaScript pada jam. Pemilihan event terjadi di firmware. Aturan sebelum sunrise, siang sebelum sunset, dan sunrise berikutnya sesudah sunset adalah target perilaku; baseline belum membuktikan ketiga transisi secara lengkap. Data esok hari juga bergantung pada data firmware. Preview sunrise/sesudah sunset menggunakan event dan waktu masukan eksplisit, bukan simulasi algoritma firmware.

Cuaca mempertahankan 29 banner dan urutan baseline. Pemetaan kondisi terhadap firmware perlu diperiksa di perangkat. Suhu negatif kini menggunakan sprite minus pada `DelimiterImageIndex`, sesuai catatan format baseline. Renderer dan validator ikut memperhitungkan minus; tampilan fisiknya tetap pending.

Mode waktu mengikuti firmware. Preview dapat menampilkan AM/PM atau menghilangkannya dengan `--ampm none`. Jam dan menit memakai alignment Left dan zero padding. Nilai metrik mempertahankan alignment Center baseline. Perilaku Center pada jam tetap bagian dari checklist fisik. Alignment Right tidak digunakan karena masalah yang telah ditemukan pada V3.

## Validasi

- Batas elemen dinamis berada dalam radius 174, termasuk suhu negatif dua digit.
- Validator collision menggabungkan semua varian digit, panjang nilai, suffix, no-data, bulan, hari, banner cuaca, dan solar. Alpha di atas 48 serta detail background di atas luminansi maksimum kanal 24 menjadi obstacle.
- CircleScale dihilangkan dari data V6, sehingga gauge lama tidak mungkin muncul dari parameter binary.
- Verifikasi binary memeriksa target perangkat, ukuran blok kompresi, indeks gambar, parameter, ukuran sprite, dan piksel round-trip.
- Preview normal identik dengan rilis sebelum optimasi di luar area tanggal yang diperbesar. AOD mempertahankan alpha, geometri, dan seluruh field, dengan RGB lebih rendah.
- Uji tanggal mencakup 7 x 31 x 12 = 2.604 kombinasi untuk pemeriksaan lebar, termasuk kombinasi tanggal yang tidak ada di kalender nyata.
- Nilai uji mencakup daftar spesifikasi, ditambah 99.999 langkah, 9.999 kcal, serta suhu -99 dan 99 derajat untuk batas representasi dua digit.
- File input pengguna dipertahankan; preview tidak digunakan sebagai bukti uji fisik.

`out/validation.json` menyimpan hasil binary. Jalankan unit test sesudah build berhasil. Jangan memakai hasil unit test dari BIN lama ketika build baru gagal.

Optimasi AOD 16 September dijelaskan di [aod-power.md](aod-power.md).

Revisi tanggal: angka memakai Inter Black dengan tinggi tinta 17 px, bulan tetap kecil. Keduanya memakai aset yang sama pada normal dan AOD.
