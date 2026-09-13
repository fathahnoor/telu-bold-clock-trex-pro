# Build dan instalasi TEL-U REDLINE

## Revisi setelah uji perangkat

V3 aktif di jam pada 12 September 2026, tetapi semua elemen merah (chip T,
kapsul menit, ikon metrik) tampil biru dan posisi jam/menit meleset karena
firmware mengabaikan Alignment Right. V4 memperbaikinya dan berjalan di jam
pada hari yang sama: byte gambar ditulis BGRX dan semua teks dinamis memakai
Alignment Left dengan koordinat eksplisit. Always-on kini memakai layout dan
latar yang sama dengan tampilan utama.
Lihat [diagnosis v4](compatibility-fix-v4.md) dan penjelasan
[diagnosis v3](compatibility-fix-v3.md) untuk riwayat referensi gambar.

## Status yang sudah dibuktikan

Berkas `out/telu_trex_pro.bin` dibuat untuk Amazfit T-Rex Pro legacy dengan
layar 360 x 360. Signature UIHH versi 2, body terkompresi, gambar 32-bit
dengan urutan byte BGRX (terbukti dari uji jam 12 September 2026), 45 gambar
termasuk preview 220 x 220 pada ID firmware 45 (indeks lokal 44).
Tampilan idle memakai background ID 1 yang sama dengan tampilan utama; slot
lokal 43 tidak lagi dirujuk.

Build lokal dan parser referensi watchface-js berhasil membaca parameter dan
45 gambar secara identik. Pemeriksaan geometri mencakup 99999 langkah,
9999 kalori, tiga digit denyut, baterai 100 persen, semua hari, dan mode idle.
Preview adalah simulasi layout dari ekstraksi bin, bukan tangkapan layar jam.

**Belum dibuktikan:** impor pada versi AmazFaces milik pengguna, transfer
Bluetooth sampai selesai, perilaku firmware, perubahan menit/tanggal, AM/PM,
dan persistensi setelah restart jam. Keberhasilan parse tidak menjamin semua
kombinasi HP, aplikasi, dan firmware dapat memasangnya.

## Langkah di AmazFaces

1. Salin `out/telu_redline_compat_v4.bin` ke folder Downloads di HP.
2. Pastikan jam yang dipilih adalah **Amazfit T-Rex Pro** dan masih tersambung
   dengan aplikasi pendampingnya. Resolusi yang benar adalah 360 x 360.
3. Pada AmazFaces, gunakan fitur **Add file / file lokal** bila tersedia,
   lalu pilih berkas `.bin`. Nama/menu dapat berbeda antar versi.
4. Jika file dikenali dan preview benar, pilih tindakan pemasangan ke jam
   yang tersedia dan ikuti instruksi koneksi aplikasi hingga transfer selesai.
5. Periksa waktu, pergantian menit, hari/tanggal, metrik, baterai, mode idle,
   lalu pastikan watchface tetap tersedia setelah restart jam.

Administrator AmazFaces mengonfirmasi penambahan file lokal pada beta dalam
[posting 8 September 2022](https://amazfitwatchfaces.com/forum/viewtopic.php?start=125&t=1709).
Itu adalah bukti historis keberadaan fitur, bukan jaminan dukungan versi HP
saat ini. Jangan mengganti model menjadi T-Rex biasa agar file dipaksa diterima.
Jika menu file lokal tidak ada atau transfer gagal, catat Android/iOS, versi
AmazFaces, firmware jam, tahap terakhir, dan pesan error untuk pemeriksaan lanjut.

Tidak perlu mengubah ekstensi menjadi ZIP atau membuat QR Zepp OS untuk berkas
ini. T-Rex Pro terdaftar sebagai perangkat non-Zepp OS pada
[dokumentasi resmi Zepp](https://docs.zepp.com/docs/reference/related-resources/device-list/).

## Build

```powershell
python tools/build_all.py
python -m unittest discover -s tools -p "test_*.py"
```

`out/validation.json` memuat SHA-256 dan hasil pemeriksaan build terakhir.
`tools/verify_reference.mjs` dapat dijalankan dengan Node dan path checkout
watchface-js. Tidak memerlukan instalasi package untuk membaca sumber parser.
Build tidak mengunggah berkas ke katalog AmazFaces.
