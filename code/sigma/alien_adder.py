"""Uzaylı toplama makinesi: n'nin harf vektöründen n+1'in küçük harflerini bulur.
Yalnızca (1) harf vektörü, (2) indis tablosu ind_p(letter) kullanılır."""
import sympy as sp
B = 50                                        # tablonun kapsadığı asallar (p ≤ B)
SP = list(sp.primerange(2, B+1))
LET = list(sp.primerange(2, 200000))          # harf alfabesi: LET[i] = (i+1). harf
g = {p: sp.primitive_root(p) for p in SP if p > 2}
# Uzaylının Canon Arithmeticus'u: ind[p][i] = harf i'nin mod p indisi (harf p'ye bölünmüyorsa)
ind = {p: {} for p in SP if p > 2}
for p in ind:
    dl = {pow(g[p], k, p): k for k in range(p-1)}
    for i, L in enumerate(LET):
        if L % p: ind[p][i] = dl[L % p]
idx = {L: i for i, L in enumerate(LET)}

def letters(n):  # yalnızca girdiyi hazırlamak için (insan → uzaylı çevirisi)
    return {idx[p]: e for p, e in sp.factorint(n).items()}

def alien_small_letters_of_succ(v):
    """v = n'nin harf vektörü. n+1'i bölen p ≤ B asallarını DOĞRUSAL formlarla bul."""
    out = []
    for p in SP:
        ip = idx[p]
        if v.get(ip, 0) > 0:          # p | n ⇒ p ∤ n+1 (komşu yasası)
            continue
        if p == 2:                    # a harfi yoksa n tek ⇒ n+1 çift
            out.append(p); continue
        Lp = sum(e * ind[p][i] for i, e in v.items()) % (p - 1)   # doğrusal form
        if Lp == (p - 1) // 2:        # n ≡ −1 (mod p)
            out.append(p)
    return out

# doğrulama
bad = 0; N = 100000; big = 0
for n in range(1, N):
    got = alien_small_letters_of_succ(letters(n))
    true = [p for p in SP if (n + 1) % p == 0]
    bad += (got != true)
    m = n + 1
    for p in true:
        while m % p == 0: m //= p
    big += (m > 1)
print(f"n < {N}: yanlış = {bad}")
print(f"n+1'in B={B}'den büyük bir harfi olan oran: {big/N:.3f}")
v = letters(14); print("örnek: 14 =", v, "→ 15'in küçük harfleri:", alien_small_letters_of_succ(v))
v = letters(12); print("örnek: 12 =", v, "→ 13'ün küçük harfleri:", alien_small_letters_of_succ(v), "(13 ≤ B ise bulunur)")
