## Blind SQL Injection Database Dumper

### Deskripsi
Proyek ini adalah hasil praktikum keamanan sistem informasi yang menunjukkan bagaimana teknik **Blind SQL Injection** dapat digunakan untuk mengekstrak data dari form login yang rentan.

### Tujuan
Mendemonstrasikan metode pengambilan data dari database menggunakan karakter per karakter, meskipun tidak ada respon langsung dari server terhadap kueri SQL.

### Tools yang Digunakan
- Python 3.x
- `requests`, `urllib3`, dan modul standar lainnya
- Server dengan endpoint rentan SQLi

### Cara Kerja
1. Menyisipkan payload injeksi ke parameter login (`user`).
2. Menebak isi database karakter demi karakter menggunakan fungsi `substring()`.
3. Mengecek hasil berdasarkan `status_code == 302` sebagai indikator data benar.
4. Menyusun struktur database (nama tabel, kolom, isi baris).
5. Menyimpan hasil ke dalam file `.sql`.
