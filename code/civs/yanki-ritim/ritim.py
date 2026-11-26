"""Ritim uygarlığı: n = her n vuruşta bir çalan davul."""
import math, itertools, random
from fractions import Fraction as F
from sympy import primerange

def pattern(n, L):  # davul n'in L vuruşluk yazısı
    return "".join("x" if t % n == 0 else "." for t in range(L))

def ensemble(ds, L):
    return "".join("X" if all(t % d == 0 for d in ds) else ("x" if any(t % d == 0 for d in ds) else ".") for t in range(L))

# --- ekok / ebob ---
def test_lcm_gcd():
    bad = 0
    for a in range(1, 121):
        for b in range(1, 121):
            first = next(t for t in range(1, a * b + 1) if t % a == 0 and t % b == 0)  # ilk ortak vuruş
            # ebob: ortak 'ızgara' = a ve b vuruş zamanlarının farklarının en küçüğü
            diffs = {(i * a - j * b) for i in range(b + 1) for j in range(a + 1)}
            g = min(d for d in diffs if d > 0)
            bad += first != math.lcm(a, b) or g != math.gcd(a, b)
    print(f"ekok = ilk ortak vuruş, ebob = iki davulun vuruşları arasındaki en kısa fark; a,b ≤ 120: hata {bad}")

# --- CRT = hizalama ---
def align(phases):
    """phases: [(periyot, faz)]; davul i, t ≡ faz (mod periyot) anlarında çalar. İlk ortak anı bul."""
    L = math.lcm(*[p for p, _ in phases])
    for t in range(L):
        if all(t % p == r for p, r in phases): return t, L
    return None, L

def test_crt():
    bad = 0; nonalign = 0
    for a in range(2, 16):
        for b in range(2, 16):
            for r in range(a):
                for s in range(b):
                    t, L = align([(a, r), (b, s)])
                    expected = (r - s) % math.gcd(a, b) == 0
                    bad += (t is not None) != expected
    print(f"Hizalama yasası: (a,r),(b,s) davulları ⇔ r ≡ s (mod ebob) ise hizalanır; a,b < 16 tüm fazlar: hata {bad}")
    print("  Örnek: 3, 5, 7 davulları fazlar (2,3,2) ile ilk kez t =", align([(3, 2), (5, 3), (7, 2)])[0], "(Sunzi: 23)")

# --- Öklid ritimleri ---
def bjorklund(k, n):
    a = [[1] for _ in range(k)]; b = [[0] for _ in range(n - k)]
    while len(b) > 1:
        m = min(len(a), len(b))
        new = [a[i] + b[i] for i in range(m)]
        rest = a[m:] if len(a) > m else b[m:]
        a, b = new, rest
    return "".join("x" if v else "." for s in a + b for v in s)

def bresenham(k, n):  # onset i, ⌊i n / k⌋ : hızı k/n olan koşucunun tur atma anları
    on = {(i * n) // k for i in range(k)}
    return "".join("x" if t in on else "." for t in range(n))

def rot_eq(s, t): return len(s) == len(t) and t in s + s

def euclid_examples():
    ex = [(2, 5, "Kore, Rumen, Fars"), (3, 4, "kalipso"), (3, 8, "tresillo (Küba)"), (5, 8, "cinquillo (Küba)"),
          (4, 9, "Türk aksak ritmi (Toussaint)"), (5, 12, "Güney Afrika"), (7, 12, "Batı Afrika çan"),
          (5, 16, "bossa nova"), (9, 16, "Orta Afrika"), (2, 3, "Batı Afrika"), (5, 9, "Arap"), (7, 16, "Brezilya samba")]
    print("Öklid ritimleri E(k,n) (Bjorklund algoritması = Öklid algoritması):")
    for k, n, name in ex:
        e = bjorklund(k, n)
        print(f"  E({k},{n}) = {e:16s}  {name}")
    bad = sum(not rot_eq(bjorklund(k, n), bresenham(k, n)) for n in range(1, 41) for k in range(1, n + 1))
    print(f"  Bjorklund ↔ ⌊i·n/k⌋ (koşucu ritmi) dönme denkliği, 1 ≤ k ≤ n ≤ 40: uyumsuz {bad}")

# --- yalnız koşucu (kesin rasyonel) ---
def nd(x):
    x -= math.floor(x); return min(x, 1 - x)

def delta(speeds):
    """max_t min_i ||t v_i||, tam değer ve zaman. Aday t = m/(v_a+v_b)."""
    v = sorted(set(abs(s) for s in speeds if s != 0)); best = F(-1); bt = None
    for a in range(len(v)):
        for b in range(a, len(v)):
            D = v[a] + v[b]
            for m in range(1, D):
                t = F(m, D); val = min(nd(t * x) for x in v)
                if val > best: best, bt = val, t
    return best, bt

def lonely_moments(w):
    """k koşucu, hızlar w: her koşucunun yalnız kaldığı ilk an (kesin) ve uzaklığı."""
    k = len(w); out = []
    for i, wi in enumerate(w):
        d, t = delta([wj - wi for j, wj in enumerate(w) if j != i])
        # ilk yalnızlık anı: 1/k uzaklığa ulaşılan en küçük t (aday ızgarada ara)
        first = None
        v = [abs(wj - wi) for j, wj in enumerate(w) if j != i]
        cands = sorted({F(m, D) for D in range(1, 2 * max(v) + 1) for m in range(1, D)} |
                       {F(m, k * x) for x in v for m in range(1, k * x)})
        for tt in cands:
            if min(nd(tt * x) for x in v) >= F(1, k): first = tt; break
        out.append((wi, d, t, first))
    return out

def lonely_examples():
    print("Her koşucunun yalnız anı (k koşucu, sınır 1/k):")
    for w in [(0, 1, 2), (0, 1, 3), (0, 1, 2, 3), (0, 3, 5, 9), (0, 1, 2, 3, 4), (2, 3, 5, 7, 11, 13), (1, 5, 6, 11, 16, 17, 0)]:
        res = lonely_moments(list(w))
        print(f"  hızlar {w}:")
        for wi, d, t, first in res:
            print(f"     hız {wi:2d}: en büyük uzaklık {d} (t={t}), ilk kez ≥1/{len(w)}: t={first}")

def prime_speeds():
    print("Asal hızlar (n hız + duran koşucu, sınır 1/(n+1)):")
    for n in range(2, 9):
        ps = list(primerange(2, 200))[:n]
        d, t = delta(ps)
        print(f"  ilk {n} asal {ps}: δ = {d} = {float(d):.4f}, (n+1)δ = {float((n+1)*d):.3f}, t = {t}")
    P = list(primerange(2, 60))
    for n in [3, 4]:
        worst = min(((n + 1) * delta(c)[0], c) for c in itertools.combinations(P, n))
        print(f"  {n} asal hız (asallar < 60) içinde en kötü (n+1)δ = {worst[0]} ({float(worst[0]):.3f}), hızlar {worst[1]}")

if __name__ == "__main__":
    print("Notasyon: 3 =", pattern(3, 12), " 4 =", pattern(4, 12), " 3∧4 =", ensemble([3, 4], 24))
    test_lcm_gcd(); test_crt(); euclid_examples(); lonely_examples(); prime_speeds()
