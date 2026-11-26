"""Asama asama tum insa: her asamada mevcut noktalardan TUM dogrular ve cemberler
cizilir, TUM kesisimler eklenir. Baslangic: {0, 1}. Sayilar OEIS A333944 ile
karsilastirilir. Ayrica 60 derece baslangici {O, U, W} icin ucleme taramasi.
"""
import sys, time, itertools
import mpmath as mp
from machine import Machine, Line, Circle


def stage(M, pts, tag):
    curves = []
    seen_l, seen_c = set(), set()
    for P, Q in itertools.combinations(pts, 2):
        curves.append(M.line(P, Q))
    for C in pts:
        for P in pts:
            if P is not C:
                curves.append(M.circle(C, P))
    # ayni egriyi iki kez sayma (es dogrular / ayni cember)
    uniq = []
    for c in curves:
        if isinstance(c, Line):
            k = ("L",) + tuple(sorted((float(v) for v in normline(c)), key=lambda z: 0))
        else:
            k = ("C", float(c.C.nx), float(c.C.ny), float(c.r2.val()))
        k = tuple(round(v, 25) if isinstance(v, float) else v for v in k)
        if k not in seen_l:
            seen_l.add(k); uniq.append(c)
    for A, B in itertools.combinations(uniq, 2):
        M.meet(A, B, tag)
    return uniq


def normline(L):
    a, b, c = L.a.val(), L.b.val(), L.c.val()
    n = mp.sqrt(a * a + b * b)
    a, b, c = a / n, b / n, c / n
    if a < -1e-50 or (abs(a) < 1e-50 and b < 0):
        a, b, c = -a, -b, -c
    return (a, b, c)


def dump(M, fn):
    with open(fn, "w") as f:
        for P in M.points:
            f.write(f"{mp.nstr(P.nx, 40)} {mp.nstr(P.ny, 40)} {M.degree(P.x)} {M.degree(P.y)}\n")


def run01(nst=2):
    M = Machine(check=True)
    pts = [M.add(0, 0, "0"), M.add(1, 0, "1")]
    print(f"asama 0: {len(M.points)} nokta")
    for s in range(1, nst + 1):
        t = time.time()
        cur = list(M.points)
        nc = len(stage(M, cur, f"s{s}"))
        hist = {}
        for _, a, b in M.log:
            for d in (a, b): hist[d] = hist.get(d, 0) + 1
        print(f"asama {s}: {nc} farkli egri, {len(M.points)} nokta, en buyuk derece {M.maxdeg}, "
              f"kule derinligi {M.T.n}, derece hist {dict(sorted(hist.items()))}  ({time.time()-t:.0f}s)")
        dump(M, f"out/pts01_s{s}.txt")
    return M


class Snapshot:
    """Makineyi bir ana geri sarmak icin: yeni noktalar ve yeni kule seviyeleri silinir."""
    def __init__(self, M):
        self.M, self.n = M, len(M.points)
        self.t = M.T.n
        self.sq, self.deg, self.log = dict(M.T.sq), dict(M._deg), len(M.log)

    def restore(self):
        M = self.M
        M.points = M.points[:self.n]
        M.T.rad = M.T.rad[:self.t + 1]; M.T.sv = M.T.sv[:self.t + 1]
        M.T.sq = dict(self.sq); M._deg = dict(self.deg); M.log = M.log[:self.log]


def all_curves(M, pts):
    cs, keys = [], set()
    for P, Q in itertools.combinations(pts, 2):
        L = M.line(P, Q); k = ("L",) + tuple(mp.nstr(v, 30) for v in normline(L))
        if k not in keys: keys.add(k); cs.append(L)
    for C in pts:
        for P in pts:
            if P is not C:
                c = M.circle(C, P); k = ("C", mp.nstr(C.nx, 30), mp.nstr(C.ny, 30), mp.nstr(c.r2.val(), 30))
                if k not in keys: keys.add(k); cs.append(c)
    return cs


def run60(nst=2):
    """60 derece baslangici {O, U, W}. Asama 1 tam (ortak kule). Asama 2 tam, ama her
    kesisim kendi kulesinde hesaplanir (geri sarma): her nokta kesin, derece kesin."""
    M = Machine(check=True)
    O = M.add(0, 0, "O"); U = M.add(1, 0, "U")
    W = M.add(M.R(1) / 2, M.R(3).sqrt() / 2, "W")
    print(f"60 derece: asama 0: {len(M.points)} nokta")
    stage(M, list(M.points), "s1")
    base = list(M.points)
    print(f"asama 1: {len(base)} nokta (kesin, ortak kule derinligi {M.T.n})")
    cs = all_curves(M, base)
    print(f"asama 2: {len(cs)} farkli egri, {len(cs)*(len(cs)-1)//2} kesisim cifti")
    snap = Snapshot(M)
    found = {}
    hist = {}
    t = time.time()
    for A, B in itertools.combinations(cs, 2):
        new = M.meet(A, B, "s2")
        for P in M.points[snap.n:]:
            k = (mp.nstr(P.nx, 35), mp.nstr(P.ny, 35))
            if k not in found:
                dx, dy = M.degree(P.x), M.degree(P.y)
                found[k] = (P.nx, P.ny, dx, dy)
                for d in (dx, dy): hist[d] = hist.get(d, 0) + 1
        snap.restore()
    for P in base:
        found.setdefault((mp.nstr(P.nx, 35), mp.nstr(P.ny, 35)), (P.nx, P.ny, 0, 0))
    pts = list(found.values())
    print(f"asama 2: {len(pts)} farkli nokta; yeni noktalarin koordinat derecesi hist {dict(sorted(hist.items()))}; "
          f"hepsi 2^k: {all(d & (d-1) == 0 for d in hist)}  ({time.time()-t:.0f}s)")
    best_ray = min(abs(mp.degrees(mp.atan2(y, x)) - 20) for x, y, _, _ in pts if abs(x) + abs(y) > 0)
    best_pair = mp.inf; hits = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            ang = mp.degrees(mp.atan2(pts[j][1] - pts[i][1], pts[j][0] - pts[i][0])) % 60
            e = min(abs(ang - 20), abs(ang - 40))
            if e < best_pair: best_pair = e
            if e < 1e-30: hits += 1
    print(f"   en iyi: O'dan isin |arg-20| = {mp.nstr(best_ray, 6)} derece; iki nokta yonu (mod 60) -> 20/40: "
          f"{mp.nstr(best_pair, 6)} derece; tam isabet: {hits}")
    with open("out/pts60_s2.txt", "w") as f:
        for x, y, dx, dy in pts:
            f.write(f"{mp.nstr(x, 30)} {mp.nstr(y, 30)} {dx} {dy}\n")
    return M


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    run01(n)
    run60()
