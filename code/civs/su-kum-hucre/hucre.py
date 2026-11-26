"""HUCRE uygarligi: yerel kurallar. Collatz'in hucresel otomat (Kari tipi, taban 6)
ve etiket sistemi (De Mol 2-tag) kodlamalari; Kural 30/110, Yasam Oyunu ornekleri."""
import numpy as np, math
from scipy.stats import kstest

# ---------- Collatz: taban-6 hucresel otomat, yaricap 1, 12 durum ----------
# Durum = (rakam 0..5, u) ; u=1 "birler basamagi" isareti. Sag komsu = daha az anlamli basamak.
def local_rule(left, me, right):
    d, u = me; dr, ur = right
    nd = 3 * (d % 2) + dr // 2                # x3, tasima yok (3 | 6)
    if u == 1:                                # birler hucresi
        if d % 2 == 1: return (4, 1)          # 3n+1: son basamak 3 -> 4, nokta yerinde
        else: return (0, 0)                   # n cift: son basamak 0, nokta sola kayar
    nu = 1 if (ur == 1 and dr % 2 == 0) else 0
    return (nd, nu)

def ca_step(cells):
    Z = (0, 0); n = len(cells)
    return [local_rule(cells[i-1] if i > 0 else Z, cells[i], cells[i+1] if i+1 < n else Z) for i in range(n)]

def encode(n, width):
    ds = []
    while n: ds.append(n % 6); n //= 6
    ds = ds + [0] * (width - len(ds))
    cells = [(x, 0) for x in reversed(ds)] + [(0, 0)] * 2   # sagda 2 kesir hucresi
    cells[width - 1] = (cells[width - 1][0], 1)
    return cells

def decode(cells):
    k = next(i for i, c in enumerate(cells) if c[1] == 1); v = 0
    for d, _ in cells[:k+1]: v = 6 * v + d
    return v

def collatz(n): return n // 2 if n % 2 == 0 else 3 * n + 1

def verify_ca(nmax):
    bad = 0; steps = 0
    for n in range(1, nmax + 1):
        # genislik: yorunge maksimumunun basamagi + sag kayma payi
        m = n; mx = n; L = 0
        while m != 1: m = collatz(m); mx = max(mx, m); L += 1
        w = len(np.base_repr(mx, 6)) + L + 2
        cells = encode(n, w); m = n
        while m != 1:
            cells = ca_step(cells); m = collatz(m); steps += 1
            if decode(cells) != m: bad += 1; break
    return bad, steps

# ---------- De Mol 2-etiket sistemi: a->bc, b->a, c->aaa ----------
P = {'a': 'bc', 'b': 'a', 'c': 'aaa'}
def tag_T(n):
    """a^n'den baslayip bir sonraki saf a^m kelimesine kadar calistir. (m, adim)"""
    w = 'a' * n; s = 0
    while True:
        if len(w) < 2: return None, s
        w = w[2:] + P[w[0]]; s += 1
        if set(w) == {'a'}: return len(w), s

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

# ---------- Kural 30 / 110, Yasam Oyunu ----------
def eca(rule, width, steps, init=None):
    x = np.zeros(width, np.uint8); x[width // 2] = 1
    rows = [x]
    tbl = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    for _ in range(steps):
        idx = (np.roll(x, 1) << 2) | (x << 1) | np.roll(x, -1)
        x = tbl[idx]; rows.append(x)
    return np.array(rows)

def life_step(g):
    n = sum(np.roll(np.roll(g, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0))
    return ((n == 3) | ((g == 1) & (n == 2))).astype(np.uint8)

if __name__ == "__main__":
    bad, steps = verify_ca(3000)
    print(f"Collatz CA (taban 6, 12 durum, yaricap 1): n<=3000, {steps} adim, {bad} hata")
    print("Ornek n=7:", end=" ")
    c = encode(7, 12); out = [7]
    for _ in range(16): c = ca_step(c); out.append(decode(c))
    print(out)
    # kural tablosunun gercekten 12^3 girdili sabit bir tablo oldugunu dogrula
    S = [(d, u) for d in range(6) for u in (0, 1)]
    table = {(l, m, r): local_rule(l, m, r) for l in S for m in S for r in S}
    print("Kural tablosu girdisi:", len(table))

    bad = 0; tot_steps = []
    for n in range(2, 5001):
        m, s = tag_T(n)
        if m != T(n): bad += 1
        tot_steps.append((n, s))
    print(f"De Mol etiket sistemi: 2<=n<=5000, a^n -> a^T(n), {bad} hata")
    ok = all(s == n + (n % 2) for n, s in tot_steps)
    print("Bir T-adimi icin etiket adimi = n + (n mod 2):", ok)
    tot = 0
    for n in range(2, 5001):
        m = n
        while m != 1: tot += m + (m % 2); m = T(m)
    print("n<=5000 icin 1'e kadar toplam etiket adimi:", tot)
    # Kural 30 merkez sutunu
    R = eca(30, 2 * 10001 + 1, 10000); col = R[:, R.shape[1] // 2]
    print(f"Kural 30 merkez sutun (10001 bit): 1 orani={col.mean():.4f}")
    for p in range(1, 2001):
        if np.array_equal(col[-4000:][p:], col[-4000:][:-p]): print("periyot", p); break
    else: print("Son 4000 bitte <=2000 periyot yok")
    R = eca(110, 401, 200); print("Kural 110: 200 adimdan sonra canli hucre:", int(R[-1].sum()))
    g = np.zeros((20, 20), np.uint8); g[1, 2] = g[2, 3] = g[3, 1] = g[3, 2] = g[3, 3] = 1
    h = g.copy()
    for _ in range(4): h = life_step(h)
    print("Yasam Oyunu planor: 4 adim sonra (1,1) kaymis kopya:", np.array_equal(h, np.roll(np.roll(g, 1, 0), 1, 1)))

    # Kari'nin x3/2 otomati ve Mahler: {(3/2)^t} mod 1 dagilimi
    fr = []; num = 1
    for t in range(1, 3001):
        num *= 3   # (3/2)^t = 3^t / 2^t
        fr.append((num % (1 << t)) / (1 << t))
    print("{(3/2)^t}, t<=3000: KS uniform p =", round(kstest(fr, 'uniform').pvalue, 3),
          "; ortalama", round(float(np.mean(fr)), 4), "; <1/2 orani", round(float(np.mean(np.array(fr) < 0.5)), 4))
