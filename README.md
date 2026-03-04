
=============================================================================================================================
RC5 Cipher — Python Implementation
Implementasi algoritma kriptografi RC5-32/12/b menggunakan Python murni (tanpa library eksternal). RC5 adalah block cipher simetris yang dirancang oleh Ronald L. Rivest (1994), dengan ciri khas data-dependent rotation — jumlah rotasi bit ditentukan oleh nilai data yang sedang diproses.

-----------------------------------------------------------------------------------------------------------------------------

Spesifikasi Algoritma
Parameter	Nilai	      Keterangan
W	        32 bit	    Ukuran word; satu blok = dua word = 8 byte
R	        12	        Jumlah putaran enkripsi/dekripsi
b	        variabel	  Panjang kunci dalam byte (ditentukan saat runtime)
P32	      0xB7E15163	Konstanta dari bilangan e (Euler)
Q32	      0x9E3779B9	Konstanta dari golden ratio 

-----------------------------------------------------------------------------------------------------------------------------

Struktur Program
rc5.py
├── rotl(x, n)          — rotasi kiri 32-bit
├── rotr(x, n)          — rotasi kanan 32-bit
├── add(a, b)           — penjumlahan mod 2³²
├── sub(a, b)           — pengurangan mod 2³²
├── key_expand(key)     — penjadwalan kunci → 26 subkunci
├── encrypt(plain, S)   — enkripsi blok 8 byte
├── decrypt(cipher, S)  — dekripsi blok 8 byte
└── __main__            — antarmuka CLI interaktif

-----------------------------------------------------------------------------------------------------------------------------

Cara Penggunaan
Prasyarat: Python 3.x (tidak ada dependensi eksternal)
python rc5.py

Program akan meminta input secara interaktif:
=== RC5 Enkripsi / Dekripsi ===
Masukkan kunci      : <kunci-rahasia>
Pilih mode [e=enkripsi / d=dekripsi] : e
Masukkan plaintext  : <pesan>
Ciphertext : <output>

-----------------------------------------------------------------------------------------------------------------------------

Cara Kerja
1. Key Expansion
Kunci pengguna diperluas menjadi 26 subkunci 32-bit (tabel S) melalui tiga fase:
    1.	Konversi — kunci bytes dimasukkan ke array word L (little-endian)
    2.	Inisialisasi — tabel S diisi dari P32 dengan step Q32
    3.	Mixing — S dan L dicampur selama 3 × max(26, c) iterasi

Fase 3 — mixing
S[i] = rotl(S[i] + A + B, 3)              # S dirotasi 3 bit (tetap)
L[j] = rotl(L[j] + A + B, (A + B) % W)    # L dirotasi data-dependent

2. Enkripsi
Setiap blok 8 byte diproses sebagai dua word A dan B:
A = add(A, S[0]); B = add(B, S[1])         # whitening awal

for r in range(1, R + 1):                  # 12 putaran
    A = add(rotl(A ^ B, B % W), S[2*r])
    B = add(rotl(B ^ A, A % W), S[2*r+1])

3. Dekripsi
Kebalikan sempurna dari enkripsi — round dibalik, + → −, rotl → rotr:
for r in range(R, 0, -1):                  # mundur: 12 → 1
    B = rotr(sub(B, S[2*r+1]), A % W) ^ A
    A = rotr(sub(A, S[2*r]),   B % W) ^ B

A = sub(A, S[0]); B = sub(B, S[1])         # undo whitening

=============================================================================================================================

