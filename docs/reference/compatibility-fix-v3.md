# Compatibility v3: referensi gambar firmware

## Hasil uji pengguna pada v2

Watchface masuk koleksi tetapi preview hitam. Saat dipilih, pilihan kembali ke
watchface default pertama. Status aktivasi v2: gagal pada jam pengguna.

## Akar kesalahan yang ditemukan

Aset proyek bernama 0.png, 1.png, dan seterusnya. Packer sebelumnya menganggap
nomor itu sama dengan ID gambar firmware. Empat berkas pembanding menunjukkan
bahwa ID firmware dimulai dari 1 dan menunjuk entri tabel pada posisi ID-1.
Parser watchface-js mengembalikan daftar gambar biasa mulai posisi 0 dan tidak
memvalidasi hubungan semantik antara ID parameter dan gambar yang dirujuk.

Contoh langsung:

| Berkas pembanding | ID background | ID preview | Hasil resolusi ID-1 |
| --- | --- | --- | --- |
| trexpro_ref.bin | 1 | 79 | 360x360 dan 220x220 |
| 17828.bin | 1 | 100 | 360x360 dan 220x220 |
| 18411.bin | 2 | 1 | 360x360 dan 220x220 |
| 18234.bin | 1 | tidak ada | 360x360 |

Pada v2, Background.ImageIndex=0 tidak merujuk gambar valid. Preview.ImageIndex=44
mengarah ke posisi tabel 43, yaitu latar idle hitam 360x360, bukan preview.
Angka jam dimulai dari ID 3, yang mengarah ke badge PM pada posisi tabel 2.
Ini cocok dengan preview hitam dan kegagalan aktivasi yang dilaporkan.

## Perubahan v3

- Nomor aset internal tetap dimulai dari 0 agar file sumber dan renderer konsisten.
- Packer mengubah semua ImageIndex, NoDataImageIndex, dan BackgroundImageIndex
  menjadi ID firmware dengan menambah 1. Koordinat, jumlah gambar, tipe data,
  dan angka bukan referensi gambar tidak diubah.
- Background sekarang ID 1; preview ID 45; angka jam pertama ID 4; idle ID 44.
- Validator me-resolve seluruh ID/range terhadap tabel gambar, memeriksa
  ukuran background dan preview yang benar-benar dirujuk.
- `build/telu/firmware_params.json` dan `build/verified_bin/firmware_params.json`
  menyimpan ID firmware asli. `watchface.json` di folder tersebut memakai
  indeks lokal mulai 0 untuk rendering.
- Urutan hari dikoreksi menjadi MON..SUN. Audit sprite dari trexpro_ref.bin
  dan 17828.bin dengan ID-1 menunjukkan Senin sebagai entri pertama.
  Urutan TUE..MON yang dicatat sebelumnya adalah akibat kesalahan indeks.

Dua tes baru gagal pada v2 sebelum perbaikan: resolusi background/preview serta
sprite angka nol. Sesudah perbaikan, sembilan tes lulus. Parser referensi
membaca 45 gambar identik. QuickLZ Java menghasilkan data identik untuk 367
blok dan 2032 byte tail. Preview baru diperiksa secara visual.

Perbaikan kompresi dan device ID dari v2 tetap dipakai. V2 disimpan untuk
pembanding dan tidak ditimpa. Belum ada klaim v3 berhasil aktif pada jam.

## Uji berikutnya

Gunakan **out/telu_redline_compat_v3.bin** melalui jalur pemasangan yang sama.
Di koleksi, preview seharusnya menampilkan REDLINE merah-putih. Pilih watchface,
periksa jam dan tanggal, lalu pastikan tetap aktif setelah restart.
Ukuran dan SHA-256 terkini ada pada `out/validation.json`.
