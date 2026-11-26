"""Kesir-merdiveni uygarliginin 'kolay' yasalari: sayisal testler."""
import math, random, time, numpy as np, mpmath as mp
from fractions import Fraction
from cf import convergents, cf_rational
from reals import cf_interval, cf_mp

LOG2 = math.log(2)
def gk(k):  # Gauss-Kuzmin P(a=k)
    return -math.log2(1 - 1 / (k + 1) ** 2)
K0 = float(mp.khinchin)
LEVY = math.pi ** 2 / (12 * LOG2)

def best_approx_test(name, xfn, Qmax=10**6, D=60):
    """2. tur en iyi yaklasim: |q x - p| rekorlari = yaklasim paydalari."""
    mp.mp.dps = D + 10
    X = int(mp.floor(xfn() * 10**D)); S = 10**D
    best = None; rec = []
    for q in range(1, Qmax + 1):
        t = q * X; p = (t + S // 2) // S
        e = abs(t - p * S)
        if best is None or e < best:
            best = e; rec.append(q)
    cfa = cf_interval(X, X + 1, S)[:-1]
    dens = [c.denominator for c in convergents(cfa)]
    dens = sorted(set(d for d in dens if d <= Qmax))
    # 1. tur: |x - p/q| rekorlari; yakinsak veya yari-yakinsak mi?
    best1 = None; rec1 = []
    for q in range(1, min(Qmax, 200000) + 1):
        t = q * X; p = (t + S // 2) // S
        e = Fraction(abs(t - p * S), q)
        if best1 is None or e < best1: best1 = e; rec1.append(q)
    h = [(1, 0)]; hh, kk = [1, cfa[0]], [0, 1]
    semis = set()
    for i in range(1, len(cfa)):
        for t in range(1, cfa[i] + 1):
            semis.add(t * kk[-1] + kk[-2])
        hh.append(cfa[i] * hh[-1] + hh[-2]); kk.append(cfa[i] * kk[-1] + kk[-2])
        if kk[-1] > 10**7: break
    semis |= set(kk)
    ok1 = all(q in semis for q in rec1)
    return rec == dens, len(rec), ok1, len(rec1)

def quad_cf(P, Q, D, maxlen=100000):
    """x=(P+sqrt D)/Q, Q | D-P^2. Durum (P,Q) tekrar ederse periyodik."""
    assert (D - P * P) % Q == 0
    s = math.isqrt(D); seen = {}; out = []
    while (P, Q) not in seen:
        seen[(P, Q)] = len(out)
        a = (P + s) // Q if Q > 0 else -((P + s) // (-Q)) - 1
        out.append(a)
        P = a * Q - P; Q = (D - P * P) // Q
        if len(out) > maxlen: return out, None
    return out, seen[(P, Q)]

def lagrange_test():
    bad = 0; n = 0; maxper = 0
    for D in range(2, 20001):
        if math.isqrt(D) ** 2 == D: continue
        cfv, start = quad_cf(0, 1, D)
        n += 1
        if start is None or start != 1: bad += 1
        # yasa: sqrt(D) = [a0; a1..a_{r-1}, 2a0], palindrom
        per = cfv[1:]
        if per[-1] != 2 * cfv[0] or per[:-1] != per[:-1][::-1]: bad += 1
        maxper = max(maxper, len(per))
    # rastgele kuadratik irrasyoneller (P+sqrt D)/Q
    random.seed(2); m = 0
    for _ in range(3000):
        D = random.randrange(2, 10**6)
        if math.isqrt(D) ** 2 == D: continue
        P = random.randrange(-1000, 1000)
        Q0 = D - P * P; divs = [d for d in range(1, 200) if Q0 % d == 0]
        Q = random.choice(divs) * random.choice([1, -1])
        cfv, start = quad_cf(P, Q, D)
        m += 1
        if start is None: bad += 1
        else:
            # gercekten (P+sqrtD)/Q'ya yakinsiyor mu? (ilk 30 terim, float kontrol)
            x = (P + math.sqrt(D)) / Q
            pre, per = cfv[:start], cfv[start:]
            seq = (pre + per * 40)[:30]
            if abs(float(list(convergents(seq))[-1]) - x) > 1e-9 * max(1, abs(x)): bad += 1
    return n, m, bad, maxper

def stats(cf, name):
    a = np.array([int(x) for x in cf[1:]], dtype=object)
    n = len(a)
    la = np.array([math.log(int(x)) for x in a])
    K = math.exp(la.mean())
    # Gauss-Kuzmin varyansi ile kaba z skoru (bagimsizlik varsayimi)
    ks = np.arange(1, 10**6); p = -np.log2(1 - 1 / (ks + 1.0) ** 2)
    m1 = (np.log(ks) * p).sum(); m2 = (np.log(ks) ** 2 * p).sum()
    sd = math.sqrt(m2 - m1 ** 2) / math.sqrt(n)
    z = (la.mean() - math.log(K0)) / sd
    # Levy: ln q_n / n
    r = 1.0; lq = 0.0
    for x in a:
        r = int(x) + 1.0 / r if r else float(x); lq += math.log(r)
    # dogru recursion: q_n/q_{n-1} = a_n + q_{n-2}/q_{n-1}
    rr = 0.0; lq = 0.0
    for x in a:
        rr = 1.0 / (int(x) + rr); lq -= math.log(rr)
    lev = lq / n
    freq = [np.sum(a == k) / n for k in range(1, 6)]
    big = {K_: sum(1 for x in a if x >= K_) for K_ in (10, 100, 1000, 10000)}
    return dict(name=name, n=n, K=K, z=z, levy=lev, freq=freq, big=big, max=max(a), argmax=int(np.argmax([int(x) for x in a])) + 1)

if __name__ == '__main__':
    t = time.time()
    print("== En iyi yaklasim (2. tur rekorlar = yakinsak paydalari, q<=1e6) ==")
    for nm, f in [('pi', lambda: mp.pi), ('e', lambda: mp.e), ('sqrt2', lambda: mp.sqrt(2)), ('cbrt2', lambda: mp.cbrt(2))]:
        print(nm, best_approx_test(nm, f))
    print("== Lagrange ==", lagrange_test(), f"{time.time()-t:.0f}s")
    print("== Gauss-Kuzmin / Khinchin / Levy ==  K0=%.6f  Levy=%.6f" % (K0, LEVY))
    print("GK teorik P(1..5):", [round(gk(k), 5) for k in range(1, 6)])
    print("GK teorik P(a>=K)*n orani:", {K_: round(math.log2(1 + 1 / K_), 6) for K_ in (10, 100, 1000, 10000)})
    random.seed(7); allr = []
    for s in range(5):
        D = 20000; X = random.randrange(10**D)
        allr += cf_interval(X, X + 1, 10**D)[1:-1]
    rs = stats([0] + allr, 'rastgele(5x20000 hane)')
    print(rs)
    for nm in ['pi', 'e', 'epi', 'ln2', 'pi2', 'cbrt2', 'cbrt3', 'cbrt5', 'plastic', 'x3m3xm1', 'qrt2']:
        try: cf = np.load(f'data/{nm}.npy', allow_pickle=True).tolist()
        except FileNotFoundError: print(nm, 'yok'); continue
        print(stats(cf, nm))
    print(f"toplam {time.time()-t:.0f}s")
