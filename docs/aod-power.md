# AOD dengan intensitas lebih rendah

Revisi 16 September 2026 mempertahankan semua komponen, ukuran digit, alpha, koordinat, tanggal, sensor, cuaca, dan solar. Mode normal tidak berubah.

## Yang diubah

Transformasi warna dihitung sekali di Python saat build, menggunakan lookup table 256 nilai. Firmware membaca sprite biasa, tanpa loop, timer, animasi, atau perhitungan transformasi tambahan.

- RGB digit jam AOD dikalikan 0,70, menjadi abu-abu putih yang lebih redup.
- RGB menit AOD dikalikan 0,85 agar menit tidak terlalu gelap.
- Background AOD, termasuk logo, ikon statis, kampus, dan perimeter, dikalikan 0,55.
- Warna hitam tetap nol; detail nonzero dipertahankan minimal 1. Alpha tidak berubah.
- Digit metrik kecil, tanggal, AM/PM, dan banner dinamis tetap memakai aset normal. Tidak ada komponen yang dihapus atau data yang dihentikan.

Hanya 20 sprite waktu baru ditambahkan. Background AOD menggunakan slot yang sudah tersedia. Semua rentang metrik dan tanggal dipakai bersama untuk membatasi duplikasi aset. Jumlah operasi gambar dan ukuran buffer gambar AOD tidak dikurangi; ukuran BIN bertambah. Ini bukan klaim optimasi CPU atau pengurangan RAM firmware.

## Batas format

Watchface ini merupakan paket parameter UIHH v2 untuk T-Rex Pro, bukan aplikasi Zepp OS. Dalam skema baseline yang tervalidasi tidak ditemukan kontrol interval redraw, sampling sensor, clock CPU, atau brightness panel. Tidak ditambahkan field hasil tebakan. Waktu hanya berisi jam dan menit; tidak ada detik atau animasi sejak baseline.

[Pedoman AOD Zepp](https://docs.zepp.com/docs/designs/customization/screen-off-mode/) menjadi konteks desain saja. API Zepp OS tidak diterapkan pada paket legacy ini. Mempercepat generator atau memperkecil kompresi BIN tidak otomatis mengurangi konsumsi baterai saat AOD menyala.

## Bukti dan pengukuran

`out/aod-analysis.json` dihitung dari gambar hasil ekstraksi BIN pada sembilan waktu. Ukurannya adalah jumlah nilai kanal RGB, bukan watt, luminansi fisik, atau daya tahan baterai. Penurunan sekitar 28% pada sinyal gambar tidak boleh ditafsirkan sebagai penghematan baterai 28%. Pengaruh panel, firmware, sensor, dan radio belum diukur.

`out/aod-comparison.png` memperlihatkan versi lama dan baru. `out/baseline/telu_university_v6_full_aod.bin` adalah paket sebelumnya untuk pembanding atau kembali ke AOD lama.

Untuk uji nyata, gunakan kedua BIN selama periode yang sama, idealnya 24 jam per versi, dengan jadwal AOD, brightness, koneksi HP, notifikasi, aktivitas, dan pengaturan sensor yang serupa. Catat persen awal/akhir serta durasi AOD. Ulangi bila selisih kecil karena indikator baterai dibulatkan. Jangan menyimpulkan hasil dari penurunan 1% selama beberapa menit.

Keterbacaan AOD dan penghematan baterai fisik tetap pending. Jika terlalu redup pada perangkat, gain dapat dinaikkan di `tools/gen_telu.py` tanpa mengubah desain normal.
