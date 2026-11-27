from engine_fast import Engine as Fast   # uyarlanır dallanma politikası (P3)
from engine_general import next_valid, ab, sig
from fractions import Fraction as F
import sys, time

class P2(Fast):
    ET = 4
    W = 2000
    def dfs(self, L, known, k2):
        self.nodes += 1
        if self.report and self.nodes % self.report == 0:
            print(f"  .. nodes={self.nodes} L={L} t={time.time()-self.t0:.0f}s", flush=True)
        if self.nodes > self.node_limit:
            self.unresolved.append(('limit', L, dict(known))); return
        self.maxL = max(self.maxL, L)
        r = self.force(L, known, k2)
        if r is None: return
        known, k2 = r
        T = F(self.T)
        nS = sum(1 for v in known.values() if v[0] == 'S')
        if nS > 1: return
        if k2 == 0 and nS == 0 and all(v[0] == 'E' for v in known.values()): return
        lo, hi, hik = self.bounds(L, known, k2)
        allfixed = all(v[2] is not None for v in known.values())
        exact = allfixed and k2 == 0
        if lo > T or (lo == T and k2 > 0): return
        if hi < T or (hi == T and not exact): return
        if exact:
            n = s = 1
            for p, (c, e, fx) in known.items():
                n *= p ** fx; s *= sig(p, fx)
            if s == self.T * n: self.found.append(n)
            return
        if k2 == 1 and allfixed: return
        free = [(v[1], p) for p, v in known.items() if v[2] is None]
        low = [x for x in free if x[0] <= self.ET] if k2 == 1 else []
        if k2 == 1 and not low and free and hik < T:
            # pencere genişliği tahmini: q ∈ [1/(T/lo − 1), hik/(T − hik)]
            lok = F(1)
            for p, (cls, emin, fx) in known.items():
                lok *= ab(p, fx if fx is not None else emin)
            qmax = hik / (T - hik)
            qmin = 1 / (T / lok - 1) if T / lok > 1 else F(0)
            if qmax - qmin > self.W:
                # pencereyi en çok daraltan serbest harf: p^emin en küçük
                low = [min(free, key=lambda x: x[1] ** x[0])]
        if k2 > 0 and (hik < T or not free) and (k2 >= 2 or not low):
            # L-genişletme, alt sınır atlamasıyla
            lok = F(1)
            for p, (cls, emin, fx) in known.items():
                lok *= ab(p, fx if fx is not None else emin)
            y = T / lok
            q = L
            if y > 1:
                qmin = int(1 / (y - 1))
                if qmin - 1 > q: q = qmin - 1
            while True:
                q = self.nextprime_(q)
                if q in known: continue
                bound = hik
                for t in [q] + self.next_unknown(q, known, k2 - 1):
                    bound *= F(t, t - 1)
                if bound <= T: break
                kn = dict(known); c = self.cls_of(q)
                kn[q] = [c, next_valid(c, 1), None]
                self.dfs(q, kn, k2 - 1)
            return
        emin, p = low[0] if (k2 == 1 and len(low) == 1 and low[0][0] > self.ET) else (min(low) if low else min(free))
        cls = known[p][0]
        self.maxe = max(self.maxe, emin)
        if emin > self.emax:
            self.unresolved.append(('emax', L, dict(known))); return
        e0 = next_valid(cls, emin)
        kn = dict(known); fcls = cls if cls != 'U' else ('S' if e0 % 2 else 'E')
        kn[p] = [fcls, e0, e0]
        self.dfs(L, kn, k2)
        kn = dict(known); kn[p] = [cls, next_valid(cls, e0 + 1), None]
        self.dfs(L, kn, k2)

if __name__ == '__main__':
    K = int(sys.argv[1]); ET = int(sys.argv[2]); rep = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    P2.ET = ET
    P2.W = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    E = P2(K, 2, True, emax=150, node_limit=10**9, report=rep).run()
    print(f"DONE K={K} ET={ET} nodes={E.nodes} maxL={E.maxL} maxe={E.maxe} unresolved={len(E.unresolved)} t={time.time()-E.t0:.1f}s", flush=True)
