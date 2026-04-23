# N-Queens Visualizer (Brute Force vs Backtracking)

Proyek ini adalah visualisasi interaktif untuk membandingkan dua pendekatan pada masalah N-Queens:

- Brute Force: mencoba semua kemungkinan penempatan.
- Backtracking: menelusuri solusi secara rekursif dan memangkas cabang yang tidak valid.

Repository ini menyediakan dua versi aplikasi:

- Versi web: menggunakan HTML, CSS, dan JavaScript.
- Versi desktop: menggunakan Python Tkinter.

## Fitur Utama

- Pengaturan ukuran papan N (4 sampai 10).
- Pengaturan kecepatan animasi.
- Pemilihan algoritma Brute Force atau Backtracking.
- Visualisasi langkah demi langkah proses penempatan ratu.
- Statistik eksekusi: langkah, backtrack, jumlah ratu aktif, dan waktu.
- Log proses eksekusi untuk melihat keputusan algoritma.
- Ringkasan perbandingan hasil setelah kedua algoritma dijalankan.

## Struktur Proyek

```text
nqueens-demo/
|- index.html   # Antarmuka utama versi web
|- index.css    # Styling versi web
|- script.js    # Logika visualisasi dan algoritma versi web
|- nqueens.py   # Aplikasi desktop Tkinter
```

## Prasyarat

### Untuk versi web

- Browser modern (Chrome, Edge, Firefox, atau sejenisnya).

### Untuk versi desktop

- Python 3.8 atau lebih baru.
- Tkinter (umumnya sudah bawaan instalasi Python standar).

## Cara Menjalankan

### 1) Menjalankan versi web

Opsi cepat:

1. Buka file index.html langsung di browser.

Opsi yang disarankan (melalui local server):

1. Buka terminal di folder proyek.
2. Jalankan perintah berikut:

```bash
python -m http.server 8000
```

3. Buka browser ke alamat berikut:

```text
http://localhost:8000
```

### 2) Menjalankan versi desktop (Tkinter)

1. Buka terminal di folder proyek.
2. Jalankan perintah berikut:

```bash
python nqueens.py
```

## Cara Menggunakan Aplikasi

1. Atur nilai N sesuai ukuran papan yang diinginkan.
2. Atur kecepatan animasi.
3. Pilih algoritma (Backtracking atau Brute Force).
4. Klik tombol mulai untuk menjalankan visualisasi.
5. Amati papan, statistik, dan log eksekusi.
6. Klik reset untuk mengulang dari kondisi awal.
7. Jalankan kedua algoritma untuk melihat perbandingan performa.

## Ringkasan Algoritma

### Backtracking

- Menempatkan ratu per baris.
- Mengecek keamanan posisi sebelum lanjut ke baris berikutnya.
- Jika buntu, mundur ke keputusan sebelumnya (backtrack).
- Cocok untuk menunjukkan efek pruning pada ruang solusi.

Kompleksitas waktu (worst case): O(N!)

### Brute Force

- Menghasilkan semua permutasi kemungkinan penempatan kolom.
- Mengecek validitas setiap permutasi.
- Tidak melakukan pruning secara cerdas.

Kompleksitas waktu: O(N! x N)

## Catatan

- Performa sangat dipengaruhi oleh nilai N.
- Untuk N yang lebih besar, Brute Force akan jauh lebih lambat dibanding Backtracking.
- Nilai waktu dapat berbeda tergantung spesifikasi perangkat dan kecepatan animasi.

## Konteks

Proyek ini cocok untuk materi Strategi Algoritma (misalnya IF2211) dalam topik:

- Exhaustive search (Brute Force)
- Pruning dan backtracking
- Analisis perbandingan performa algoritma