"""OYUN uygarlığı: kombinatoryal oyunlar {L|R}, sürreal sayılar, Nim, nimber çarpımı."""
from functools import lru_cache
from fractions import Fraction
from itertools import product

# ---------- Genel oyun: G = (L, R), L ve R oyunların frozenset'i ----------
def G(L=(), R=()): return (frozenset(L), frozenset(R))
ZERO = G()

@lru_cache(maxsize=None)
def le(g, h):
    """g <= h  <=>  g'nin hiçbir sol seçeneği >= h değil ve h'nin hiçbir sağ seçeneği <= g değil."""
    return not any(le(h, gl) for gl in g[0]) and not any(le(hr, g) for hr in h[1])
def eq(g, h): return le(g, h) and le(h, g)

@lru_cache(maxsize=None)
def add(g, h):
    return (frozenset([add(x, h) for x in g[0]] + [add(g, y) for y in h[0]]),
            frozenset([add(x, h) for x in g[1]] + [add(g, y) for y in h[1]]))
@lru_cache(maxsize=None)
def neg(g): return (frozenset(neg(x) for x in g[1]), frozenset(neg(x) for x in g[0]))

def from_dyadic(x, cache={}):
    """İkili-kesirli x için en basit sürreal oyunu kur (doğum günü kuralı)."""
    x = Fraction(x)
    if x in cache: return cache[x]
    if x == 0: g = ZERO
    elif x.denominator == 1:
        n = int(x); g = G([from_dyadic(n-1)]) if n > 0 else G((), [from_dyadic(n+1)])
    else:
        d = Fraction(1, x.denominator); g = G([from_dyadic(x-d)], [from_dyadic(x+d)])
    cache[x] = g; return g

# ---------- Doğum günleri ----------
def simplest_between(lo, hi):
    """lo < x < hi aralığındaki en basit ikili kesir (lo/hi None olabilir)."""
    if lo is None and hi is None: return Fraction(0)
    if lo is None: return min(Fraction(0), Fraction(int(hi) - 1 if hi == int(hi) else int(hi // 1)))
    if hi is None: return max(Fraction(0), Fraction(int(lo // 1) + 1))
    if lo < 0 < hi: return Fraction(0)
    # en küçük paydalı (sonra en küçük mutlak değer) sayı
    d = 1
    while True:
        import math
        k = math.floor(lo * d) + 1
        if Fraction(k, d) < hi:
            cands = [Fraction(j, d) for j in range(k, math.ceil(hi * d)) ]
            return min(cands, key=abs)
        d *= 2

def numbers_by_day(n):
    days = [{Fraction(0)}]
    for _ in range(n):
        old = sorted(set().union(*days))
        new = set(old)
        # {L|R} için yalnız max L ve min R önemli
        opts = [None] + old
        for a in opts:
            for b in opts:
                if a is not None and b is not None and not a < b: continue
                new.add(simplest_between(a, b))
        days.append(new - set().union(*days))
    return days

def games_by_day(n):
    """n. güne kadar doğan tüm oyunların eşdeğerlik sınıfı sayısı (sadece n<=2)."""
    reps = [ZERO]
    for _ in range(n):
        subsets = []
        for mask in range(1 << len(reps)):
            subsets.append([reps[i] for i in range(len(reps)) if mask >> i & 1])
        newreps = []
        for L, R in product(subsets, subsets):
            g = G(L, R)
            if not any(eq(g, h) for h in newreps): newreps.append(g)
        reps = newreps
    return reps

# ---------- Mavi-Kırmızı Hackenbush (dizi) ----------
@lru_cache(maxsize=None)
def hack_game(s):
    """s: yerden yukarı 'B'/'R' dizisi. Bir kenarı kesmek üstünü de düşürür."""
    return (frozenset(hack_game(s[:i]) for i in range(len(s)) if s[i] == 'B'),
            frozenset(hack_game(s[:i]) for i in range(len(s)) if s[i] == 'R'))

def berlekamp(s):
    """Berlekamp kuralı: ilk renk değişimine kadar tam sayı, sonra ikiye bölünen adımlar."""
    if not s: return Fraction(0)
    sign = 1 if s[0] == 'B' else -1
    k = 0
    while k < len(s) and s[k] == s[0]: k += 1
    v = Fraction(sign * k); step = Fraction(1)
    if k < len(s):
        v -= sign * Fraction(1, 2); step = Fraction(1, 2)
        for c in s[k+1:]:
            step /= 2; v += step if c == 'B' else -step
    return v

# ---------- Nim ve Sprague–Grundy ----------
def mex(s):
    m = 0
    while m in s: m += 1
    return m

def grundy_sum(heaps, moves):
    """Toplam oyunun Grundy değeri, doğrudan (XOR kullanmadan) mex ile."""
    @lru_cache(maxsize=None)
    def g(state):
        opts = set()
        for i, h in enumerate(state):
            for m in moves(h):
                nxt = list(state); nxt[i] = h - m
                opts.add(g(tuple(sorted(nxt))))
        return mex(opts)
    return g(tuple(sorted(heaps)))

# ---------- Nimber çarpımı ----------
@lru_cache(maxsize=None)
def nim_mul_def(a, b):
    """Conway tanımı: a*b = mex{ a'b + ab' + a'b' : a'<a, b'<b } (+ = XOR)."""
    return mex({nim_mul_def(x, b) ^ nim_mul_def(a, y) ^ nim_mul_def(x, y)
                for x in range(a) for y in range(b)})

@lru_cache(maxsize=None)
def nim_mul(a, b, half=32):
    """Hızlı: Fermat 2-kuvvetleri F=2^(2^k) ile böl; F*F = 3F/2."""
    if a < 2 or b < 2: return a * b
    while half > 1 and max(a, b) < (1 << half): half //= 2
    F = 1 << half
    a1, a0 = divmod(a, F); b1, b0 = divmod(b, F)
    hi = nim_mul(a1, b1, half)
    mid = nim_mul(a1, b0, half) ^ nim_mul(a0, b1, half) ^ hi
    lo = nim_mul(a0, b0, half) ^ nim_mul(hi, F >> 1, half)
    return (mid << half) ^ lo
