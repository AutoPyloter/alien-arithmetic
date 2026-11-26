"""Görev 2-3: p ve q = floor(alpha*p + beta) + c ikisi de asal çiftlerinin sayımı.
Kullanım: python3 beatty_pairs.py X   (varsayılan 10^8)
q tam sayı aritmetiğiyle kesin hesaplanır (float + sınır düzeltmesi)."""
import sys, math, time
import numpy as np
from fractions import Fraction
import mpmath
from sieve import segment, small_primes, mr

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
mpmath.mp.dps = 120
SH = 256
C2 = 0.66016181584686957392  # ikiz asal sabiti

def fixed(v):  # floor(v * 2^SH)
    return int(mpmath.floor(v * mpmath.mpf(2) ** SH))

PHI = (1 + mpmath.sqrt(5)) / 2
# (ad, alpha (float), kesin floor fonksiyonu x -> floor(alpha*x+beta), c, rasyonel (a,b) veya None)
def make_fixed(alpha_mp, beta_mp):
    A, B = fixed(alpha_mp), fixed(beta_mp)
    return lambda x: (x * A + B) >> SH  # hata < (x+1)/2^256: 1e9 icin ihmal

CASES = [
 # ad, alpha_mp, beta_mp, c, rasyonel
 ("phi (altın kaydırma: floor((p+1)phi)-1)", PHI, PHI, -1, None),
 ("phi, c=0", PHI, 0, 0, None),
 ("phi, c=1", PHI, 0, 1, None),
 ("sqrt2, c=0", mpmath.sqrt(2), 0, 0, None),
 ("sqrt2, c=1", mpmath.sqrt(2), 0, 1, None),
 ("sqrt3, c=0", mpmath.sqrt(3), 0, 0, None),
 ("e, c=0", mpmath.e, 0, 0, None),
 ("pi, c=0", mpmath.pi, 0, 0, None),
 ("pi, c=1", mpmath.pi, 0, 1, None),
 ("3/2, c=0", None, None, 0, (3, 2)),
 ("3/2, c=1", None, None, 1, (3, 2)),
 ("3/2, c=2", None, None, 2, (3, 2)),
 ("3/2, c=-1", None, None, -1, (3, 2)),
 ("5/3, c=0 (phi yaklaşığı)", None, None, 0, (5, 3)),
 ("8/5, c=0 (phi yaklaşığı)", None, None, 0, (8, 5)),
 ("13/8, c=0 (phi yaklaşığı)", None, None, 0, (13, 8)),
 ("7/5, c=0 (sqrt2 yaklaşığı)", None, None, 0, (7, 5)),
 ("2, c=1 (Sophie Germain)", None, None, 1, (2, 1)),
 ("1, c=2 (ikiz asal)", None, None, 2, (1, 1)),
]

def prime_factors(n):
    n = abs(n); f = set(); d = 2
    while d * d <= n:
        while n % d == 0: f.add(d); n //= d
        d += 1
    if n > 1: f.add(n)
    return f

def singular_rational(a, b, c):
    """Yerel çarpanlar çarpımı S(a/b, c); p = b k + r, q = a k + floor(a r/b) + c."""
    units = [r for r in range(b) if math.gcd(r, b) == 1]
    Pa, Pab = prime_factors(a), prime_factors(a * b)
    base = C2
    for l in Pab:
        if l >= 3: base /= l * (l - 2) / (l - 1) ** 2
    tot = 0.0
    for r in units:
        d = (a * r) // b + c; s = (a * r) % b
        m = b * c - s  # l ∤ ab ve l | m ise çakışma (q≡0 ile p≡0 aynı k'da)
        if m == 0: return float('inf')
        val = base
        for l in Pa: val *= (l / (l - 1)) if d % l else 0.0  # l | a: q ≡ d (mod l) sabit
        if 2 not in Pab: val *= 2.0 if m % 2 == 0 else 0.0  # l=2 temel çarpanı 0, çakışmada 2
        for l in prime_factors(m):
            if l in Pab or l == 2: continue
            val *= (l / (l - 1)) / (l * (l - 2) / (l - 1) ** 2)
        tot += val
    return tot / len(units)

def brute_singular(a, b, c, L=200):
    """Kontrol: küçük l'ler için doğrudan sayım, l>L için kuyruk ~ 1."""
    from sieve import small_primes
    units = [r for r in range(b) if math.gcd(r, b) == 1]; tot = 0
    for r in units:
        v = 1.0
        for l in small_primes(L):
            l = int(l); good = cnt = 0
            for k in range(l):
                n = b * k + r; q = a * k + (a * r) // b + c
                if n % l: cnt += 1; good += (q % l != 0)
            v *= (good / cnt) / (1 - 1 / l)
        tot += v
    return tot / len(units)

if __name__ == "__main__":
    t0 = time.time()
    # asallık tablosu: 0..QMAX (bool, ~QMAX bayt)
    QMAX = int(3.2 * X) + 10
    base = small_primes(math.isqrt(QMAX) + 1)
    isp = np.empty(QMAX + 1, bool); seg = 10**7
    for lo in range(0, QMAX + 1, seg):
        hi = min(lo + seg, QMAX + 1); isp[lo:hi] = segment(lo, hi, base)
    P = np.nonzero(isp[:X + 1])[0].astype(np.int64)
    print(f"elek: {QMAX:.3g}'e kadar, {time.time()-t0:.1f} sn; pi(X)={len(P)}", flush=True)
    # bağımsız kontrol: rastgele 2000 sayıda elek = Miller-Rabin
    rng = np.random.default_rng(1); smp = rng.integers(0, QMAX, 2000)
    assert all(bool(isp[v]) == mr(int(v)) for v in smp); print("elek ↔ Miller-Rabin örnek kontrolü: tamam")
    marks = [10**k for k in range(4, 12) if 10**k <= X]
    if X not in marks: marks.append(X)
    idx = np.searchsorted(P, marks, 'right')
    Pf = P.astype(np.float64)
    rows = []
    for name, al, be, c, rat in CASES:
        t1 = time.time()
        if rat:
            a, b = rat; q = (a * P) // b + c
            S = singular_rational(a, b, c); Sb = brute_singular(a, b, c)
        else:
            f = make_fixed(al, be); af, bf = float(al), float(be)
            v = Pf * af + bf; q = np.floor(v).astype(np.int64)
            fr = v - q; bad = np.nonzero((fr < 1e-5) | (fr > 1 - 1e-5))[0]
            for i in bad: q[i] = f(int(P[i]))
            # örnek tam kontrol
            for i in rng.integers(0, len(P), 3000): assert q[i] == f(int(P[i]))
            q = q + c; S = Sb = 1.0
        ok = (q >= 2) & isp[np.clip(q, 0, QMAX)]
        w = np.where(q >= 3, 1.0 / np.log(np.maximum(q, 3).astype(np.float64)), 0.0)
        cobs = np.cumsum(ok); cmod = np.cumsum(w)
        out = []
        for x, j in zip(marks, idx):
            o, m = int(cobs[j - 1]), float(cmod[j - 1])
            out.append((x, o, m, o / m))
        rows.append((name, S, Sb, out))
        print(f"\n{name}: S(teori)={S:.4f} S(kaba sayım, l<200)={Sb:.4f}  [{time.time()-t1:.1f} sn]")
        for x, o, m, r in out:
            print(f"  x={x:.0e}  gözlenen={o:>9d}  saf model={m:>12.1f}  oran={r:.4f}  oran/S={r/S if S>0 else float('nan'):.4f}")
    print(f"\ntoplam süre {time.time()-t0:.1f} sn")
