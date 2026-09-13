# Riset format v5 — cuaca, matahari, dan nama bulan

Catatan ini merangkum temuan yang dipakai untuk membangun edisi
**TELKOM UNIVERSITY**. Semua diverifikasi silang lewat dua jalur:

1. **Dump bin referensi** — file `.bin` T-Rex Pro yang sudah beredar
   (`trexpro_ref.bin`, sampel `17828`, `18234`, `18411`).
2. **Sumber editor komunitas** — proyek C# watchface editor (SashaCX75) yang
   jadi acuan penamaan field.

## Modul cuaca (Weather)

- `Type: 8` adalah cuaca. Ada dua bagian:
  - **Suhu** lewat `NumberSequence` (digit), plus `SuffixImage` untuk `°C`,
    `NoDataImageIndex` untuk kondisi tanpa data, dan `DelimiterImageIndex`
    yang dipakai firmware untuk tanda minus pada suhu negatif.
  - **Ikon kondisi** lewat `4:Linear` dengan `ImageRange.ImagesCount = 29`.
    Jumlah 29 ini **tetap** — urutan kondisi mengikuti standar internal
    firmware. Urutan di proyek ini adalah tebakan terbaik berdasarkan
    ikon-ikon yang tersedia di referensi; kalau di jam ada ikon yang tidak
    pas, cukup tukar urutan file banner lalu build ulang.
- Label kondisi (SUNNY, CLOUDY, dst.) ditanam langsung ke dalam gambar banner,
  jadi tidak membutuhkan font sistem.

## Modul matahari (Sunrise / Sunset)

- `Type: 12` adalah matahari. Semua sampel memakai **sub-blok
  `NumberSequence` tanpa `Type`** — di editor ini setara dengan tombol
  **"Closest sunrise / sunset"**: firmware otomatis memilih jam terbit
  (sebelum tengah hari) atau jam terbenam (setelahnya).
- `4:Linear` dengan `ImagesCount = 2` adalah pasangan ikon
  **terbit / terbenam** — ikon + label kita tanam di gambar, dipilih
  otomatis mengikuti keadaan yang sama dengan jamnya.
- `DecimalPointImageIndex` dipakai untuk titik dua `:` di antara jam dan
  menit (`18:02`).
- Keuntungan desain: **satu modul** untuk dua keadaan — tidak perlu
  mengganti-ganti watchface sepanjang hari.

## Tanggal & nama bulan

- `YearMonthDay` dengan `Type: 1` = bulan sebagai **gambar bernama**
  (12 gambar, Januari–Desember). `Type: 2` = hari (angka + zero padding).
- `Week` = 7 gambar urutan **MON..SUN** (sudah terverifikasi di perangkat
  pada edisi v4, kasus "SAT 12").

## Delimiter dan DecimalPoint

- `DelimiterImageIndex` dipakai di `NumberSequence` angka ribuan (langkah)
  untuk koma pemisah: `8,426`.
- `DecimalPointImageIndex` dipakai di jam (titik dua) dan bisa juga untuk
  angka desimal lain bila diperlukan.

## Batasan yang tetap berlaku (dari v4)

- Firmware T-Rex Pro **tidak menghormati `Alignment: Right`** — semua teks
  memakai `Alignment: Left` dengan posisi X yang dihitung sendiri.
- Urutan byte gambar **BGRX** (bukan RGBA) di dalam blok terkompresi.
- Semua referensi gambar di parameter **mulai dari 1**, sedangkan nama file
  lokal mulai dari 0 (packer yang menaikkan).

## Checklist saat menguji di jam

- [ ] Ikon cuaca sesuai dengan kondisi di layar (kalau tidak, tukar urutan
      banner `87`–`115`).
- [ ] Modul matahari berganti sendiri dari terbit (pagi) ke terbenam (sore).
- [ ] Koma ribuan tampil di angka langkah.
- [ ] Tanda minus tampil saat suhu negatif (opsional, Indonesia umumnya aman).
- [ ] Always-on tetap menampilkan jam, hari, tanggal, dan baterai.
