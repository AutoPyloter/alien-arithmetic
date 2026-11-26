"""Collatz haritasi 2-adik dunyada.
T(x) = x/2 (cift), (3x+1)/2 (tek).  Q(x) = parite dizisi, 2-adik sayi olarak okunur:
Q(x) = Σ v_i 2^i,  v_i = T^i(x) mod 2."""
from fractions import Fraction
from math import gcd
from itertools import product
import sys

def T(n):  # tamsayi (negatif de) uzerinde
    return n >> 1 if n % 2 == 0 else (3*n + 1) >> 1

def Qk(n, k):
    """n'nin ilk k paritesi, ikili sayi olarak (v_0 en sag hane)."""
    v = 0
    for i in range(k):
        if n & 1: v |= 1 << i
        n = T(n)
    return v

def check_permutation(kmax=20):
    out = []
    for k in range(1, kmax+1):
        N = 1 << k
        img = [Qk(n, k) for n in range(N)]
        perm = len(set(img)) == N
        # sadece kalan sinifina bagli mi? n ve n+2^k (ve n-2^k) ayni k-parite
        dep = all(Qk(n, k) == Qk(n + N, k) == Qk(n - 3*N, k) for n in range(min(N, 4096)))
        out.append((k, perm, dep))
    return out

# ---------- Rasyonel T-donguleri ----------
def cycle_point(v):
    """Parite kelimesi v (uzunluk p) icin T^p(x)=x olan tek 2-adik nokta.
    T^p(x) = 3^m x / 2^p + c/2^p  =>  x = c / (2^p - 3^m)."""
    x_lin_a, x_lin_b = Fraction(1), Fraction(0)  # x -> a x + b
    for bit in v:
        if bit: x_lin_a, x_lin_b = 3*x_lin_a/2, (3*x_lin_b + 1)/2
        else:   x_lin_a, x_lin_b = x_lin_a/2, x_lin_b/2
    return x_lin_b / (1 - x_lin_a)

def Tq(x):  # rasyonel (tek payda) uzerinde T
    a, d = x.numerator, x.denominator
    return x/2 if a % 2 == 0 else (3*x + 1)/2

def primitive(v):
    p = len(v)
    return all(v != v[r:]+v[:r] for r in range(1, p) if p % r == 0)

def cycles(pmax):
    res = []
    for p in range(1, pmax+1):
        seen = set()
        for v in product((0,1), repeat=p):
            if not primitive(v): continue
            canon = min(v[r:]+v[:r] for r in range(p))
            if canon in seen: continue
            seen.add(canon)
            x = cycle_point(canon)
            orb = [x]
            for _ in range(p-1): orb.append(Tq(orb[-1]))
            assert Tq(orb[-1]) == x
            res.append((p, sum(canon), canon, orb))
    return res

def necklaces(p):  # ilkel ikili kolye sayisi (Moebius)
    def mu(n):
        r, q = 1, 2
        while q*q <= n:
            if n % q == 0:
                n //= q
                if n % q == 0: return 0
                r = -r
            q += 1
        return -r if n > 1 else r
    return sum(mu(p//d) * 2**d for d in range(1, p+1) if p % d == 0) // p

def ordmod(d, b=2):
    if d == 1: return 1
    k, x = 1, b % d
    while x != 1: x = x*b % d; k += 1
    return k

# ---------- Q'nun rasyoneller uzerinde kesin hesabi ----------
def Q_exact(x, maxsteps=10**6):
    """x rasyonel, tek payda. Yorunge (1/d)Z icinde kalir (3x+d problemi), bir donguye
    girerse Q(x) rasyonel: onperiyot + periyot kelimesinden hesapla. Basarisizsa None."""
    x = Fraction(x)
    d = x.denominator
    a = x.numerator
    seen = {}
    bits = []
    i = 0
    while a not in seen:
        if i > maxsteps or abs(a) > 10**60: return None
        seen[a] = i
        b = a & 1
        bits.append(b)
        a = (a >> 1) if b == 0 else (3*a + d) >> 1
        i += 1
    s = seen[a]
    pre, per = bits[:s], bits[s:]
    P = sum(b << j for j, b in enumerate(pre))
    W = sum(b << j for j, b in enumerate(per))
    L = len(per)
    return Fraction(P) + Fraction(2**s * W, 1 - 2**L)

if __name__ == '__main__':
    print('== Q mod 2^k permutasyon mu? (k, permutasyon, yalniz n mod 2^k ye bagli)')
    for row in check_permutation(20): print('  ', row)
    print()
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    cs = cycles(PMAX)
    print(f'== Ilkel periyotlu tum 2-adik T-donguleri, p <= {PMAX}')
    from collections import Counter
    cnt = Counter(c[0] for c in cs)
    for p in range(1, PMAX+1):
        print(f'  p={p:2d}: {cnt[p]:4d} dongu  (ilkel kolye sayisi {necklaces(p)})')
    print('  Tamsayi donguler:')
    for p, m, v, orb in cs:
        if all(o.denominator == 1 for o in orb):
            print(f'    p={p} m={m} kelime={"".join(map(str,v))} nokta={[int(o) for o in orb]}')
    print('  p<=4 tum donguler (en kucuk |x|):')
    for p, m, v, orb in cs:
        if p <= 4:
            D = 2**p - 3**m
            print(f'    p={p} m={m} kelime={"".join(map(str,v))} 2^p-3^m={D:4d}  dongu={[str(o) for o in orb]}')
    # isaret: tum noktalar ayni isarette; isaret = sign(2^p - 3^m)
    ok = all(all((o > 0) == (2**p > 3**m) for o in orb) for p, m, v, orb in cs if m > 0)
    print('  isaret yasasi (m>0 icin tum noktalar sign(2^p-3^m) isaretli):', ok)
    # indirgenmis payda dongu boyunca sabit mi; ikili periyot
    ok = all(len({o.denominator for o in orb}) == 1 for *_, orb in cs)
    print('  dongu boyunca indirgenmis payda sabit:', ok)
    # Cift-periyodik donguler: noktanin ikili periyodu p'yi boler
    dp = [(p, m, v, orb) for p, m, v, orb in cs if p % ordmod(orb[0].denominator) == 0]
    print(f'  "cift periyodik" donguler (ikili periyot(x) | p): {len(dp)} adet')
    for p, m, v, orb in dp:
        d = orb[0].denominator
        print(f'    p={p} m={m} kelime={"".join(map(str,v))} payda={d} ord_d(2)={ordmod(d)} '
              f'gcd(2^p-1,3^m-1)={gcd(2**p-1, 3**m-1)}')
