"""Görev 4: altın uygarlığın diğer doğal soruları."""
import math, time, numpy as np
from sympy import isprime
from sieve import primes_upto, mr
F = [1, 2]
while F[-1] < 10**20: F.append(F[-1] + F[-2])     # Zeckendorf harfleri 1,2,3,5,8,...
def zeck(n):
    s = []
    for f in reversed(F):
        if f <= n: s.append('1'); n -= f
        else: s.append('0')
    return ''.join(s).lstrip('0') or '0'
def val(s): return sum(F[i] for i, c in enumerate(reversed(s)) if c == '1')
def sh(n): m = n + 1; return (m + math.isqrt(5 * m * m)) // 2 - 1

print("=== (a) Altın Fibonacci asalları ===")
# kaydır(F_k) = F_{k+1}: tek harfli kelime sola kayınca bir sonraki harf olur
assert all(sh(F[i]) == F[i + 1] for i in range(len(F) - 1)); print("kaydır(F_k)=F_{k+1}: F_k < 1e20 için doğru")
fp = [f for f in F if isprime(f)]
print("Fibonacci asalları (<1e20):", fp)
print("p ve kaydır(p) ikisi de Fibonacci asalı:", [(f, sh(f)) for f in fp if isprime(sh(f))])
# kaydır(p) Fibonacci asalı olan p (p asal, herhangi): kaydır'ın tersi tek, p = kaydır^{-1}(F_{k+1}) = F_k
print("Teorem: F_n asal => n asal ya da n=4. Ardışık indeksler ikisi de {asal}∪{4} => sadece (2,3),(3,5).")

print("\n=== (b) Altın Cunningham zincirleri: p, s(p), s(s(p)), ... hepsi asal ===")
X = 10**7
P = primes_upto(X)
t = time.time()
chains = {}
lens = []
for p in P.tolist():
    L = 1; q = p
    while True:
        q = sh(q)
        if mr(q): L += 1
        else: break
    lens.append(L)
lens = np.array(lens)
for k in range(2, 8):
    obs = int((lens >= k).sum())
    # model: prod_{j=1}^{k-1} 1/ln s^j(p)  (s^j(p) ~ p phi^j)
    lp = np.log(P.astype(float)); phi = (1 + 5 ** .5) / 2
    mod = np.prod([1 / (lp + j * math.log(phi)) for j in range(1, k)], axis=0).sum()
    print(f"  p<=1e7, zincir uzunluğu >= {k}: gözlenen {obs:7d}, bağımsızlık modeli {mod:10.1f}, oran {obs / mod:.3f}")
best = int(P[lens.argmax()]); ch = [best]
for _ in range(lens.max() - 1): ch.append(sh(ch[-1]))
print("  en uzun zincir:", ch, [zeck(c) for c in ch[:2]], f"({time.time() - t:.0f} sn)")
print("  en küçük başlangıçlar, uzunluk k için:", {k: int(P[np.argmax(lens >= k)]) for k in range(2, lens.max() + 1)})

print("\n=== (c) Zeckendorf palindromik asallar ===")
def pals(L):
    h = (L + 1) // 2; out = []
    def rec(s):
        if len(s) == h:
            if L % 2 == 0:
                if s[-1] == '1' and L > 1: return
                full = s + s[::-1]
            else: full = s + s[-2::-1]
            out.append(full); return
        for c in '01':
            if c == '1' and s[-1] == '1': continue
            rec(s + c)
    rec('1'); return out
t = time.time(); tot = pr = 0; model = 0.0; bins = []
div = {2: 0, 3: 0, 5: 0, 7: 0, 11: 0}
for L in range(1, 57):
    vs = [val(s) for s in pals(L)]
    c = sum(1 for v in vs if v > 1 and mr(v)); m = sum(1 / math.log(v) for v in vs if v > 2)
    for v in vs:
        for d in div: div[d] += (v % d == 0)
    tot += len(vs); pr += c; model += m
    if L % 8 == 0: bins.append((L, tot, pr, model))
for L, n, c, m in bins: print(f"  uzunluk <= {L:2d} (değer < {F[L]:.2e}): {n:7d} palindrom, {c:6d} asal, model Σ1/ln n = {m:9.1f}, oran {c / m:.3f}")
print("  palindromların küçük asallara bölünme oranı (beklenen 1/l):", {d: round(div[d] / tot, 4) for d in div})
print("  ilk palindromik asallar:", [(v, zeck(v)) for v in sorted(val(s) for L in range(1, 12) for s in pals(L)) if v > 1 and isprime(v)][:14], f"({time.time() - t:.0f} sn)")

print("\n=== (d) Zeckendorf'ta 1 sayısı (hane toplamı) ===")
X = 10**8
P = primes_upto(X).astype(np.int64)
def digsum(a):
    a = a.copy(); c = np.zeros(len(a), np.int64)
    for f in reversed([f for f in F if f <= X]):
        m = a >= f; a -= f * m; c += m
    return c
s = digsum(P)
for x in (10**6, 10**7, 10**8):
    ss = s[P <= x]
    print(f"  p<=1e{int(math.log10(x))}: tek sayıda 1 oranı {np.mean(ss % 2 == 1):.5f} ; mod 3 dağılımı {np.round(np.bincount(ss % 3) / len(ss), 5)} ; (N={len(ss)}, std≈{0.5/len(ss)**.5:.5f})")
allx = digsum(np.arange(1, 10**7 + 1))
print(f"  tüm n<=1e7: tek sayıda 1 oranı {np.mean(allx % 2 == 1):.5f}")
