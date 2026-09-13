# TEL-U REDLINE compatibility revision 2

## Gejala dari pengguna

Zepp mencapai 100%, jam restart lalu kembali ke watchface existing. Opsi Add to
collection dan Replace current watchface memberi hasil yang sama. Tidak ada
bukti bahwa versi lama sempat tampil atau berhasil tersimpan permanen.

## Kesalahan yang dibuktikan

1. Offset 16 pada header memakai device ID 59 dari template. Empat sampel
   T-Rex Pro lokal memakai 83. Packer kini menulis 83 secara eksplisit.
2. Header QuickLZ menyatakan hasil 4096 byte, tetapi compressor lama menghasilkan
   blok 32768 byte. Decoder Python dan watchface-js mengabaikan deklarasi ini.
   Implementasi QuickLZ Java dari GTR2_Packer justru gagal membaca file lama:
   `ArrayIndexOutOfBoundsException: Index 4096 out of bounds for length 4096`.
3. Marker pada offset 75 bernilai 255; semua empat sampel bernilai 1. Packer
   kini mengikuti nilai sampel. Makna lengkap byte tersebut belum ditentukan.

Ketidakcocokan kompresi adalah penjelasan kuat untuk kegagalan setelah transfer,
namun penyebab pada firmware jam belum dapat dipastikan tanpa hasil uji ulang.
Tampilan dan parameter UI tidak diubah dalam revisi ini.

## Perbaikan dan bukti

- QuickLZ level 3 menggunakan blok 4096 byte, ukuran packed dan decoded uint32
  yang benar, empat literal terakhir, serta jarak match minimal tiga byte.
- Bagian akhir kurang dari 4096 byte ditulis mentah seperti tool komunitas.
- Decoder QuickLZ Java: 367 blok, 2032 byte tail, seluruh hasil identik.
- Parser watchface-js: parameter serta semua 45 gambar identik.
- Tujuh tes regresi lulus. Berkas lama ditolak validator ID perangkat;
  setelah hanya ID-nya diperbaiki, masih ditolak validator ukuran kompresi.
- Kandidat baru `out/telu_redline_compat_v2.bin`: 200476 byte.
- SHA-256: `ba96d8e1033cbe5f53ef62118c93f6cd7674142758284d960a8c22db507a2a93`.

Perbandingan menggunakan empat sampel lokal dari audit proyek sebelumnya:
`trexpro_ref.bin`, `17828.bin`, `18234.bin`, `18411.bin` di folder Temp/opencode/binref.
Tiga memakai kompresi, satu tidak. Sampel tersebut belum dinyatakan pernah
terpasang pada jam pengguna. Metadata header lain yang belum dipahami tetap
mengikuti template; belum ada klaim pemeriksaan checksum firmware lengkap.

## Uji ulang

Salin file dengan nama **telu_redline_compat_v2.bin**, pilih berkas itu secara
langsung agar tidak memakai unduhan lama. Gunakan jalur pemasangan yang tadi
sudah mencapai 100%. Pastikan tampilan REDLINE muncul, dapat dipilih dalam
koleksi jam, dan tetap aktif setelah restart. Hasil perangkat masih pending.

## Reproduksi validasi

```powershell
python tools/build_all.py
python -m unittest discover -s tools -p "test_*.py"
node --experimental-vm-modules tools/verify_reference.mjs "PATH_TO_WATCHFACE_JS"
```

Untuk QuickLZ independen, ekstrak raw body memakai `decompress_uihh`, lalu:

```powershell
java --class-path "PATH_TO_GTR2_Packer.exe" tools/VerifyQuickLZ.java out/telu_redline_compat_v2.bin build/audit/fixed.raw
```

Tool Java yang sudah tersedia di laptop digunakan lewat classpath, tanpa
instalasi package. Implementasi QuickLZ asli lebih ketat daripada parser
watchface-js yang dipakai dalam pemeriksaan pertama.

Referensi format: [QuickLZ 1.5.0](https://github.com/ReSpeak/quicklz/blob/master/Format.md).
Header panjang menyimpan ukuran compressed dan decompressed secara terpisah.
