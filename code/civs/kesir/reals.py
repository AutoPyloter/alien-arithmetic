"""Gercek sayilarin surekli kesir katsayilari (titiz yontemler).
1) Aralik yontemi: x, [X, X+1]/10^N icinde ise iki ucun SK'lerinin ortak oneki dogrudur.
2) Polinom yontemi (Lagrange): x, tamsayi katsayili P'nin >1 tek gercek koku ise
   a=floor(x), P(a+1/y)*y^d yeni polinom. Tamamen tamsayi, hata yok."""
import sys, time, numpy as np
import mpmath as mp

def cf_interval(lo_p, hi_p, q, nmax=None):
    """[lo_p/q, hi_p/q] araligindaki her sayinin ortak SK oneki."""
    out = []
    a, b = (lo_p, q), (hi_p, q)
    while True:
        if a[1] == 0 or b[1] == 0: break
        x, y = a[0] // a[1], b[0] // b[1]
        if x != y: break
        # Aralik daralinca q==0 durumlari: tam bolunme ucta
        out.append(x)
        if nmax and len(out) >= nmax: break
        a = (a[1], a[0] - x * a[1]); b = (b[1], b[0] - x * b[1])
    return out

def cf_mp(expr_fn, digits, nmax=None):
    mp.mp.dps = digits + 20
    x = expr_fn()
    N = 10 ** digits
    X = int(mp.floor(x * N))
    cf = cf_interval(X, X + 1, N, nmax)
    return cf[:-1]  # son katsayiyi guvenlik icin at

def cf_poly(coeffs, nterms):
    """coeffs: P'nin katsayilari, en yuksek dereceden. P'nin >=1 tek koku varsayilir
    (ilk adimda x>1 icin en buyuk gercek kok). Python tamsayilari, kesin."""
    P = [int(c) for c in coeffs][::-1]  # P[i] = x^i katsayisi
    d = len(P) - 1
    def ev(P, k):
        s = 0
        for c in reversed(P): s = s * k + c
        return s
    def sgn(v): return (v > 0) - (v < 0)
    def shift(P, a):  # P(x+a)
        P = P[:]
        for i in range(d):
            for j in range(d - 1, i - 1, -1):
                P[j] += a * P[j + 1]
        return P
    out = []
    for _ in range(nterms):
        # kok > 1 araligi: [k, k+1) bul, isaret degisimi ile
        s1 = sgn(ev(P, 1))
        lo, hi = 1, 2
        while sgn(ev(P, hi)) == s1: lo, hi = hi, hi * 2
        while hi - lo > 1:
            m = (lo + hi) // 2
            if sgn(ev(P, m)) == s1: lo = m
            else: hi = m
        a = lo
        out.append(a)
        Q = shift(P, a)
        P = Q[::-1]          # y^d * Q(1/y)
        if P[d] < 0: P = [-c for c in P]
    return out

def cf_algebraic(coeffs, a0, nterms):
    """x = a0 + 1/x1; x1 icin polinom kur ve cf_poly'ye ver."""
    P = [int(c) for c in coeffs][::-1]; d = len(P) - 1
    for i in range(d):
        for j in range(d - 1, i - 1, -1):
            P[j] += a0 * P[j + 1]
    P = P[::-1]
    return [a0] + cf_poly(P[::-1], nterms - 1)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    jobs = {
        'cbrt2':  ([1, 0, 0, -2], 1),
        'cbrt3':  ([1, 0, 0, -3], 1),
        'cbrt5':  ([1, 0, 0, -5], 1),
        'plastic': ([1, 0, -1, -1], 1),   # x^3=x+1
        'x3m3xm1': ([1, 0, -3, -1], 1),  # tamamen gercek kubik, en buyuk kok 1.879
        'qrt2':   ([1, 0, 0, 0, -2], 1),  # 2^(1/4), derece 4
    }
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for name, (c, a0) in jobs.items():
        if only and name not in only: continue
        t = time.time()
        cf = cf_algebraic(c, a0, n)
        np.save(f'data/{name}.npy', np.array(cf, dtype=object))
        print(name, cf[:15], f'{time.time()-t:.1f}s', flush=True)
