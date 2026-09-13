# Rata tengah metrik dan tanggal v5

Nilai STEPS, BPM, POWER, dan KCAL memakai `Alignment: Center` pada parameter
BIN. Posisi X menyatakan awal kotak digit maksimum, bukan koordinat pusat.
Kotak ini menampung 5 digit langkah, 3 digit BPM, 3 digit baterai, atau
4 digit kalori. Posisi baterai mengimbangi lebar suffix persen agar angka
dan persen berada di tengah sebagai satu kelompok. Label statis tetap
berpusat pada koordinat masing-masing cincin.

Perhitungan mengikuti fungsi `Draw_dagital_text` pada
[sumber editor SashaCX75](https://github.com/SashaCX75/AmazFit_Watchface_Editor_2/blob/master/GTR_Watch_face/PreviewToBitmap.cs).
Renderer lokal serta validator diperbarui mengikuti semantik kotak tersebut.
Catatan v4 tentang alignment Right adalah hasil pengamatan versi lama;
pengamatan itu tidak membuktikan bahwa koordinat X merupakan titik jangkar.
Hasil alignment Center pada firmware perangkat tetap memerlukan uji langsung.

Tanggal menggunakan format `Fri, 12 Sep`, sesuai pilihan pengguna. Seluruh
karakternya memakai Cascadia Mono Bold 13 px, putih, dengan baseline 14 px
di dalam sprite setinggi 18 px. Setiap karakter memiliki advance 8 px.
Baris berisi 11 karakter termasuk spasi, lebarnya 88 px, dan dimulai pada
X=136 di layar 360 px. Tanggal selalu dua digit sehingga lebar tidak berubah.
Font dan lisensi SIL OFL tersedia dalam `assets/fonts/`.

Mode normal dan always-on memakai parameter serta aset yang sama.

## Pemeriksaan build

- 20 test lulus, termasuk pemusatan angka pada seluruh panjang digit yang
  digunakan, pemusatan 2.604 kombinasi hari/tanggal/bulan, dan kesamaan
  piksel preview always-on dengan normal.
- Deviasi pusat tinta terhadap pusat yang dituju maksimal 0,5 piksel dalam
  skenario uji, karena pembulatan posisi raster.
- Validator layout lulus pada aset sumber dan hasil ekstraksi BIN.
- Batas lingkaran lulus. Parameter dan piksel hasil ekstraksi BIN sama
  dengan sumber; ukuran dan SHA-256 ada di `out/validation.json`.
- Preview harian, nilai nol, dan nilai maksimum ditinjau secara visual.

Ini validasi build dan simulasi. Belum ada hasil uji firmware baru untuk
perubahan rata tengah ini.
