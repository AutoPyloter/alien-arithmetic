"""
Genel zorlama motoru: σ(n) = T·n, ω(n) = K.
- odd=True: n tek; T = 2 ise Euler sınıfları (tam bir özel harf) kullanılır.
- odd=False: 2 de aday asal; sınıf kısıtı yok.
Kesin rasyonel aritmetik. Doğrulama amacıyla bilinen çözümleri bulmalı.
"""
from fractions import Fraction as F
from sympy import nextprime, factorint
import sys, time
sys.setrecursionlimit(100000)


def sig(p, e):
    return (p ** (e + 1) - 1) // (p - 1)


def ab(p, e):
    return F(sig(p, e), p ** e)


def valid(cls, e):
    if e < 1:
        return False
    if cls == 'E':
        return e % 2 == 0
    if cls == 'S':
        return e % 4 == 1
    if cls == 'U':
        return e % 4 != 3
    return True  # 'A': her üs


def next_valid(cls, e):
    e = max(e, 1)
    while not valid(cls, e):
        e += 1
    return e


class Engine:
    def __init__(self, K, T=2, odd=True, emax=120, node_limit=10**7, report=0):
        self.K, self.T, self.odd = K, T, odd
        self.euler = odd and T == 2
        self.emax, self.node_limit = emax, node_limit
        self.nodes = 0
        self.unresolved, self.found = [], []
        self.fc = {}
        self.maxL = self.maxe = 0
        self.report = report
        self.vT = factorint(T)
        self.t0 = time.time()

    def cls_of(self, q):
        if not self.euler:
            return 'A'
        return 'E' if q % 4 == 3 else 'U'

    def factor(self, n):
        f = self.fc.get(n)
        if f is None:
            f = factorint(n)
            self.fc[n] = f
        return f

    def nextprime_(self, q):
        return nextprime(q)

    def next_unknown(self, L, known, k):
        out, q = [], L
        while len(out) < k:
            q = nextprime(q)
            if q not in known:
                out.append(q)
        return out

    def run(self):
        L0 = 2 if self.odd else 1
        self.dfs(L0, {}, self.K)
        return self

    def force(self, L, known, k2):
        changed = True
        while changed:
            changed = False
            contrib = {}
            for p, (cls, emin, fx) in known.items():
                if fx is None:
                    continue
                for r, v in self.factor(sig(p, fx)).items():
                    contrib[r] = contrib.get(r, 0) + v
            # T'nin asalları için v_r(n) = v_r(σ) − v_r(T) ≥ 0 sonra kontrol
            for r, v in contrib.items():
                need = v - self.vT.get(r, 0)       # v_r(n) ≥ need
                if r not in known:
                    if need <= 0:
                        continue                   # r ∤ n mümkün (yalnızca T'nin asalları)
                    if r <= L or k2 == 0:
                        return None
                    if self.odd and r == 2:
                        return None
                    known = dict(known)
                    c = self.cls_of(r)
                    known[r] = [c, next_valid(c, 1), None]
                    k2 -= 1
                    changed = True
                cls, emin, fx = known[r]
                if fx is not None:
                    if need > fx:
                        return None
                elif need > emin:
                    ne = next_valid(cls, need)
                    if ne > self.emax:
                        self.unresolved.append(('emax', L, dict(known)))
                        return None
                    known = dict(known)
                    known[r] = [cls, ne, None]
                    changed = True
            if changed:
                continue
        return known, k2

    def bounds(self, L, known, k2):
        lo = hi = F(1)
        for p, (cls, emin, fx) in known.items():
            if fx is not None:
                a = ab(p, fx); lo *= a; hi *= a
            else:
                lo *= ab(p, emin); hi *= F(p, p - 1)
        hik = hi
        for q in self.next_unknown(L, known, k2):
            hi *= F(q, q - 1)
        return lo, hi, hik

    def dfs(self, L, known, k2):
        self.nodes += 1
        if self.report and self.nodes % self.report == 0:
            print(f"  .. nodes={self.nodes} L={L} t={time.time()-self.t0:.0f}s", flush=True)
        if self.nodes > self.node_limit:
            self.unresolved.append(('limit', L, dict(known)))
            return
        self.maxL = max(self.maxL, L)
        r = self.force(L, known, k2)
        if r is None:
            return
        known, k2 = r
        T = F(self.T)
        if self.euler:
            nS = sum(1 for v in known.values() if v[0] == 'S')
            if nS > 1:
                return
            if k2 == 0 and nS == 0 and all(v[0] == 'E' for v in known.values()):
                return
        lo, hi, hik = self.bounds(L, known, k2)
        allfixed = all(v[2] is not None for v in known.values())
        exact = allfixed and k2 == 0
        if lo > T or (lo == T and k2 > 0):
            return
        if hi < T or (hi == T and not exact):
            return
        if exact:
            n = s = 1
            for p, (c, e, fx) in known.items():
                n *= p ** fx; s *= sig(p, fx)
            if s == self.T * n:
                self.found.append(n)
            return
        free = [(v[1], p) for p, v in known.items() if v[2] is None]
        if k2 > 0 and (hik < T or not free):
            q = L
            while True:
                q = self.nextprime_(q)
                if q in known:
                    continue
                bound = hik
                for t in [q] + self.next_unknown(q, known, k2 - 1):
                    bound *= F(t, t - 1)
                if bound <= T:
                    break
                kn = dict(known)
                c = self.cls_of(q)
                kn[q] = [c, next_valid(c, 1), None]
                self.dfs(q, kn, k2 - 1)
            return
        emin, p = min(free)
        cls = known[p][0]
        self.maxe = max(self.maxe, emin)
        if emin > self.emax:
            self.unresolved.append(('emax', L, dict(known)))
            return
        e0 = next_valid(cls, emin)
        kn = dict(known)
        fcls = cls if cls != 'U' else ('S' if e0 % 2 else 'E')
        kn[p] = [fcls, e0, e0]
        self.dfs(L, kn, k2)
        kn = dict(known)
        kn[p] = [cls, next_valid(cls, e0 + 1), None]
        self.dfs(L, kn, k2)


if __name__ == '__main__':
    K = int(sys.argv[1]); T = int(sys.argv[2]); odd = sys.argv[3] == 'odd'
    emax = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    E = Engine(K, T, odd, emax=emax, node_limit=5 * 10**6).run()
    print(f"K={K} T={T} {'odd' if odd else 'all'} nodes={E.nodes} maxL={E.maxL} maxe={E.maxe} "
          f"found={sorted(E.found)} unresolved={len(E.unresolved)} t={time.time()-E.t0:.1f}s")
