"""Kesir-merdiveni ve Yol uygarliklarinin cekirdek tanimlari."""
from fractions import Fraction
from math import gcd

def cf_rational(p, q):
    """p/q (q>0) icin sonlu surekli kesir [a0; a1, ..., an]."""
    out = []
    while q:
        a, r = divmod(p, q)
        out.append(a); p, q = q, r
    return out

def cf_value(a):
    """[a0;a1,...,an] -> Fraction (yaklasimlarla)."""
    h0, h1, k0, k1 = 1, a[0], 0, 1
    for x in a[1:]:
        h0, h1 = h1, x*h1 + h0
        k0, k1 = k1, x*k1 + k0
    return Fraction(h1, k1)

def convergents(a):
    h0, h1, k0, k1 = 1, a[0], 0, 1
    yield Fraction(h1, k1)
    for x in a[1:]:
        h0, h1 = h1, x*h1 + h0
        k0, k1 = k1, x*k1 + k0
        yield Fraction(h1, k1)

def sb_path(p, q):
    """Pozitif p/q icin Stern-Brocot yolu (1/1'den), dogrudan agac inisiyle.
    Mediant araması: sol sinir a/b, sag sinir c/d."""
    assert p > 0 and q > 0
    a, b, c, d = 0, 1, 1, 0
    path = []
    while True:
        m, n = a + c, b + d
        if p * n == q * m:
            return ''.join(path)
        if p * n < q * m:      # hedef medyantin solunda
            path.append('L'); c, d = m, n
        else:
            path.append('R'); a, b = m, n

def path_to_frac(path):
    a, b, c, d = 0, 1, 1, 0
    for s in path:
        m, n = a + c, b + d
        if s == 'L': c, d = m, n
        else: a, b = m, n
    return Fraction(a + c, b + d)

def runs(path):
    """Ardisik blok uzunluklari, R ile baslar (ilk blok 0 olabilir)."""
    out, cur, cnt = [], 'R', 0
    for s in path:
        if s == cur: cnt += 1
        else: out.append(cnt); cur = s; cnt = 1
    out.append(cnt)
    return out

def path_from_cf(a):
    """Yasa: x=[a0;a1,...,an] icin yol = R^a0 L^a1 R^a2 ... (son blok a_n - 1)."""
    a = list(a)
    a[-1] -= 1
    return ''.join(('R' if i % 2 == 0 else 'L') * k for i, k in enumerate(a))

if __name__ == '__main__':
    import random, time
    t = time.time(); bad = 0; n = 0
    for q in range(1, 301):
        for p in range(1, 301):
            if gcd(p, q) != 1: continue
            n += 1
            P = sb_path(p, q)
            if path_to_frac(P) != Fraction(p, q): bad += 1
            if path_from_cf(cf_rational(p, q)) != P: bad += 1
    print(f"Tum p,q<=300 aralarinda asal ({n} kesir): hata={bad}")
    random.seed(1); bad = 0
    for _ in range(2000):
        p, q = random.randrange(1, 10**12), random.randrange(1, 10**12)
        g = gcd(p, q); p //= g; q //= g
        a = cf_rational(p, q)
        if a[-1] == 1 and len(a) > 1: pass
        if path_from_cf(a) != sb_path(p, q) or cf_value(a) != Fraction(p, q): bad += 1
    print(f"2000 rastgele kesir (pay,payda<1e12): hata={bad}")
    # birebirlik: uzunluk<=14 tum yollar farkli kesirler
    seen = set(); tot = 0
    for L in range(0, 15):
        for m in range(2**L):
            P = ''.join('R' if (m >> i) & 1 else 'L' for i in range(L))
            seen.add(path_to_frac(P)); tot += 1
    print(f"Uzunluk<=14 tum {tot} yol -> {len(seen)} farkli kesir (birebir={tot==len(seen)})")
    print(f"sure {time.time()-t:.1f}s")
    print("ornek 3/7:", cf_rational(3, 7), sb_path(3, 7))
