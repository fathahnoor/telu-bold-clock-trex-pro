# Uji Amazfit T-Rex Pro

Status: **pending**, menunggu pemasangan oleh pengguna.

Pasang `out/telu_university_v6.bin` melalui alur file lokal T-Rex Pro yang sebelumnya berhasil. Pastikan model yang dipilih T-Rex Pro 360 x 360. Catat versi firmware, aplikasi pemasang, tanggal pengujian, dan SHA-256 BIN dari `out/validation.json`.

- [ ] BIN diterima dan preview muncul di daftar watchface.
- [ ] Jam putih, menit abu-abu terang, aksen tetap merah.
- [ ] Bandingkan `00:00`, `01:01`, `10:28`, `11:11`, dan `23:59` dengan preview.
- [ ] Angka terbaca pada jarak lengan dan lebih jauh, dibandingkan V5.
- [ ] Mode 12/24 jam, AM/PM, serta zero padding mengikuti pengaturan jam.
- [ ] Hari, tanggal, dan bulan benar serta tidak terpotong.
- [ ] Steps, BPM, kcal, persen baterai, dan koma ribuan tampil benar.
- [ ] Solar menampilkan hanya satu event, dengan label yang cocok dengan waktunya.
- [ ] Periksa solar sebelum sunrise, setelah sunrise, sebelum sunset, dan setelah sunset. Catat perilaku aktual serta sumber waktu esok hari bila tersedia.
- [ ] Ikon/label cuaca cocok dengan data Zepp, termasuk saat data tidak tersedia.
- [ ] Suhu negatif mempertahankan tanda minus bila data uji tersedia.
- [ ] AOD mempertahankan posisi jam, menit, tanggal, baterai, dan panel lain.
- [ ] Tidak ada clipping di bezel atau tumpang tindih saat nilai berubah.
- [ ] Catat konsumsi baterai AOD pada pemakaian normal. Belum ada klaim efisiensi daya.

Foto tunggal cukup untuk mencatat penampilan pada satu keadaan, tetapi tidak membuktikan transisi solar, semua nilai, atau konsumsi baterai.
