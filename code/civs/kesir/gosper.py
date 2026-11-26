"""Gosper'in iki-homografik algoritmasi: z = (axy+bx+cy+d)/(exy+fx+gy+h).
SK'leri dogrudan, terim terim toplar/carpar. Maliyet sayaci ile."""
import math, time, numpy as np, mpmath as mp
from itertools import islice
from reals import cf_mp, cf_algebraic

class Cost:
    def __init__(s): s.mults = 0; s.inx = 0; s.iny = 0; s.out = 0; s.maxbits = 0

def gosper(xs, ys, coef, nout, cost, max_in=10**7, tight=True):
    """tight=True: ilk terimler (a0) zorla alinir, sonra kuyruklar [1,inf] kutusunda
    oldugu icin koseler x,y in {1,inf}. tight=False: klasik [0,inf] kutusu (temkinli)."""
    a, b, c, d, e, f, g, h = coef
    xs, ys = iter(xs), iter(ys); xdone = ydone = False
    res = []
    def ingx(p):
        nonlocal a, b, c, d, e, f, g, h
        cost.inx += 1; cost.mults += 4
        a, b, c, d, e, f, g, h = a * p + c, b * p + d, a, b, e * p + g, f * p + h, e, f
    def ingy(q):
        nonlocal a, b, c, d, e, f, g, h
        cost.iny += 1; cost.mults += 4
        a, b, c, d, e, f, g, h = a * q + b, a, c * q + d, c, e * q + f, e, g * q + h, g
    if tight:
        ingx(next(xs)); ingy(next(ys))
    while len(res) < nout and cost.inx + cost.iny < max_in:
        cost.maxbits = max(cost.maxbits, max(abs(v).bit_length() for v in (a, b, c, d, e, f, g, h)))
        if tight:   # koseler (inf,inf),(inf,1),(1,inf),(1,1)
            N = (a, a + b, a + c, a + b + c + d); Dn = (e, e + f, e + g, e + f + g + h)
        else:       # koseler (inf,inf),(inf,0),(0,inf),(0,0)
            N = (a, b, c, d); Dn = (e, f, g, h)
        if all(v > 0 for v in Dn) or all(v < 0 for v in Dn):
            q = [n_ // d_ for n_, d_ in zip(N, Dn)]
            if q[0] == q[1] == q[2] == q[3]:
                r = q[0]; res.append(r); cost.out += 1; cost.mults += 4
                a, b, c, d, e, f, g, h = e, f, g, h, a - r * e, b - r * f, c - r * g, d - r * h
                continue
        if e == 0 and f == 0 and g == 0 and h == 0: break
        def spread(i1, i2):
            if Dn[i1] == 0 or Dn[i2] == 0: return math.inf
            from fractions import Fraction as Fr
            return abs(Fr(N[i1], Dn[i1]) - Fr(N[i2], Dn[i2]))
        sx = max(spread(1, 3), spread(0, 2))   # x degisince
        sy = max(spread(2, 3), spread(0, 1))   # y degisince
        if sx == sy: takex = (cost.inx <= cost.iny)
        else: takex = sx > sy
        takex = (takex and not xdone) or ydone
        if takex:
            p = next(xs, None)
            if p is None:
                xdone = True; a, b, c, d, e, f, g, h = 0, 0, a, b, 0, 0, e, f
                if ydone: break
                continue
            ingx(p)
        else:
            q_ = next(ys, None)
            if q_ is None:
                ydone = True; a, b, c, d, e, f, g, h = 0, a, 0, c, 0, e, 0, g
                if xdone: break
                continue
            ingy(q_)
    return res

def homographic(xs, coef, nout, cost):
    """z=(ax+b)/(cx+d), tek girdi. det(ad-bc) korunur -> durum sinirli kalir."""
    a, b, c, d = coef; xs = iter(xs); res = []
    p = next(xs); cost.inx += 1; a, b, c, d = a * p + b, a, c * p + d, c
    while len(res) < nout:
        cost.maxbits = max(cost.maxbits, max(abs(v).bit_length() for v in (a, b, c, d)))
        D1, D2 = c, c + d
        if (D1 > 0 and D2 > 0) or (D1 < 0 and D2 < 0):
            r1, r2 = a // c, (a + b) // (c + d)
            if r1 == r2:
                res.append(r1); a, b, c, d = c, d, a - r1 * c, b - r1 * d; continue
        p = next(xs); cost.inx += 1; a, b, c, d = a * p + b, a, c * p + d, c
    return res

ADD = (0, 1, 1, 0, 0, 0, 0, 1)
MUL = (1, 0, 0, 0, 0, 0, 0, 1)

def sqrt_cf(D):
    a0 = math.isqrt(D); P, Q = 0, 1
    while True:
        a = (P + a0) // Q; yield a
        P = a * Q - P; Q = (D - P * P) // Q

if __name__ == '__main__':
    def check(name, xs, ys, op, truth_fn, N, tight=True):
        c = Cost(); t = time.time()
        z = gosper(xs, ys, op, N, c, tight=tight)
        dt = time.time() - t
        tr = cf_mp(truth_fn, int(N * 1.2) + 50)[:len(z)] if truth_fn else None
        ok = (tr == z) if tr is not None else None
        print(f"{name:22s} cikti={len(z):6d} girdi x={c.inx:6d} y={c.iny:6d} "
              f"girdi/cikti={(c.inx+c.iny)/max(1,len(z)):.3f} maxbit={c.maxbits:6d} sure={dt:.2f}s dogru={ok}")
        return c, z
    print("== Gosper: toplama/carpma maliyeti ==")
    pi = np.load('data/pi.npy', allow_pickle=True).tolist()
    e = np.load('data/e.npy', allow_pickle=True).tolist()
    check('KLASIK sqrt2+sqrt3 N=2000', sqrt_cf(2), sqrt_cf(3), ADD, lambda: mp.sqrt(2) + mp.sqrt(3), 2000, tight=False)
    for N in (1000, 4000, 8000):
        check(f'sqrt2+sqrt3 N={N}', sqrt_cf(2), sqrt_cf(3), ADD, lambda: mp.sqrt(2) + mp.sqrt(3), N)
    for N in (1000, 4000, 8000):
        check(f'pi+e N={N}', pi, e, ADD, lambda: mp.pi + mp.e, N)
    for nm, co, tf in [('2*pi', (2, 0, 0, 1), lambda: 2 * mp.pi), ('(3pi+1)/(2pi+5)', (3, 1, 2, 5), lambda: (3*mp.pi+1)/(2*mp.pi+5))]:
        for N in (1000, 4000, 16000):
            c = Cost(); t = time.time(); z = homographic(pi, co, N, c); dt = time.time() - t
            ok = cf_mp(tf, int(N * 1.2) + 50)[:N] == z
            print(f"{nm+' N='+str(N):22s} girdi/cikti={c.inx/N:.3f} maxbit={c.maxbits:4d} sure={dt:.2f}s dogru={ok}")
    check('pi*e N=4000', pi, e, MUL, lambda: mp.pi * mp.e, 4000)
    check('sqrt2*sqrt3 N=4000', sqrt_cf(2), sqrt_cf(3), MUL, lambda: mp.sqrt(6), 4000)
    # Ucuz islemler, karsilastirma icin: x+1, 1/x, 2x (homografik, tek girdi)
    print("== Takilma: sqrt2*sqrt2 = 2 (tam sayi) ==")
    for M in (100, 1000, 10000):
        c = Cost(); z = gosper(sqrt_cf(2), sqrt_cf(2), MUL, 1, c, max_in=M)
        print(f"  {M} girdi terimi sonra cikti: {z}  maxbit={c.maxbits}")
