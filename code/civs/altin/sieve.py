"""Segmentli Eratosthenes eleği ve deterministik Miller-Rabin (n < 3.3e24)."""
import numpy as np, math

def small_primes(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def primes_upto(X, seg=10**7):
    """X'e kadar asallar, segment segment (bellek ~seg bayt)."""
    base = small_primes(int(math.isqrt(X)) + 1)
    out = []
    for lo in range(0, X + 1, seg):
        hi = min(lo + seg, X + 1)
        out.append(lo + np.nonzero(segment(lo, hi, base))[0])
    return np.concatenate(out)

def segment(lo, hi, base):
    """[lo,hi) aralığında asallık bayrakları."""
    s = np.ones(hi - lo, bool)
    for p in base:
        p = int(p)
        if p * p >= hi: break
        st = max(p * p, ((lo + p - 1) // p) * p)
        s[st - lo::p] = False
    for k in (0, 1):
        if lo <= k < hi: s[k - lo] = False
    return s

def is_prime_sorted(q, seg=10**7):
    """Artan olmayan sırada olmayabilir; q dizisinin her elemanı asal mı (segmentli)."""
    q = np.asarray(q, np.int64)
    order = np.argsort(q, kind='stable'); qs = q[order]
    res = np.zeros(len(q), bool)
    Q = int(qs[-1]); base = small_primes(int(math.isqrt(Q)) + 1)
    i = 0
    for lo in range(0, Q + 1, seg):
        hi = min(lo + seg, Q + 1)
        j = np.searchsorted(qs, hi, 'left')
        if j > i:
            s = segment(lo, hi, base)
            res[order[i:j]] = s[qs[i:j] - lo]
        i = j
    return res

def mr(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        if n % p == 0: return n == p
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
