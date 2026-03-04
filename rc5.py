import struct

# Konstanta magic RC5 (dari bilangan e dan golden ratio φ)
P32 = 0xB7E15163
Q32 = 0x9E3779B9
W   = 32   # word size (bit)
R   = 12   # jumlah rounds
MASK = 0xFFFFFFFF

def rotl(x, n):
    n %= W
    return ((x << n) | (x >> (W - n))) & MASK

def rotr(x, n):
    n %= W
    return ((x >> n) | (x << (W - n))) & MASK

def add(a, b):
    return (a + b) & MASK

def sub(a, b):
    return (a - b) & MASK

def key_expand(key: bytes) -> list:
    u = W // 8
    t = 2 * (R + 1)
    c = max(1, (len(key) + u - 1) // u)

    L = [0] * c
    for i in range(len(key) - 1, -1, -1):
        L[i // u] = add((L[i // u] << 8) | key[i], 0)

    S = [P32]
    for i in range(1, t):
        S.append(add(S[-1], Q32))

    A = B = i = j = 0
    for _ in range(3 * max(t, c)):
        S[i] = rotl(add(add(S[i], A), B), 3)
        A = S[i]
        L[j] = rotl(add(add(L[j], A), B), add(A, B) % W)
        B = L[j]
        i = (i + 1) % t
        j = (j + 1) % c
    return S

def encrypt(plain: bytes, S: list) -> bytes:
    pad = (8 - len(plain) % 8) % 8
    plain += b'\x00' * pad
    out = b''
    for i in range(0, len(plain), 8):
        A, B = struct.unpack_from('<II', plain, i)
        A = add(A, S[0])
        B = add(B, S[1])
        for r in range(1, R + 1):
            A = add(rotl(A ^ B, B % W), S[2 * r])
            B = add(rotl(B ^ A, A % W), S[2 * r + 1])
        out += struct.pack('<II', A, B)
    return out

def decrypt(cipher: bytes, S: list) -> bytes:
    out = b''
    for i in range(0, len(cipher), 8):
        A, B = struct.unpack_from('<II', cipher, i)
        for r in range(R, 0, -1):
            B = rotr(sub(B, S[2 * r + 1]), A % W) ^ A
            A = rotr(sub(A, S[2 * r]),     B % W) ^ B
        A = sub(A, S[0])
        B = sub(B, S[1])
        out += struct.pack('<II', A, B)
    return out.rstrip(b'\x00')

if __name__ == '__main__':
    print("=== RC5 Enkripsi / Dekripsi ===")
    key = input("Masukkan kunci      : ").encode()
    S   = key_expand(key)
    pilihan = input("Pilih mode [e=enkripsi / d=dekripsi] : ").strip().lower()

    if pilihan == 'e':
        plaintext = input("Masukkan plaintext  : ").encode()
        enc = encrypt(plaintext, S)
        print(f"Ciphertext : {enc.hex()}")
    elif pilihan == 'd':
        hex_input = input("Masukkan ciphertext : ").strip()
        cipher = bytes.fromhex(hex_input)
        dec = decrypt(cipher, S)
        print(f"Plaintext : {dec.decode(errors='replace')}")
    else:
        print("Pilihan tidak valid.")