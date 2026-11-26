"""
engine_general.py'nin hızlı sürümü (aynı mantık, aynı budama kuralları).
Fark yalnızca σ(p^e)'nin asal çarpanlarını bulma biçiminde:
  1. σ(p^e) = ∏_{d | e+1, d>1} Φ_d(p) siklotomik parçalara bölünür.
  2. Bilinen asallar ve T'nin asalları bölünerek çıkarılır.
  3. Kalan m için: gcd(m, L#) > 1 ise dışlanmış küçük asal var ⇒ buda.
     m = 1 ⇒ tamam. Boş yuva yoksa ⇒ buda. m asal ya da asal kuvveti ⇒ tek yeni asal.
     Yalnızca bir yuva varsa ve m başka bir şeyse ⇒ buda. Aksi halde tam çarpanlara ayır.
Hepsi tam (kesin) adımlar; sezgisel budama yok.
"""
import gmpy2
from gmpy2 import mpz, is_prime, next_prime, gcd, iroot
from sympy import factorint, divisors
from engine_general import Engine as Base, sig
import sys, time

class Engine(Base):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.prim = {}
        self.cyc = {}
        self.fallback = 0

    def nextprime_(self, q):
        return int(next_prime(q))

    def next_unknown(self, L, known, k):
        out, q = [], L
        while len(out) < k:
            q = int(next_prime(q))
            if q not in known:
                out.append(q)
        return out

    def primorial(self, L):
        L = min(L, 100000)   # yalnızca kısayol: L'den küçük asallar sonra force'ta da yakalanır
        v = self.prim.get(L)
        if v is None:
            if len(self.prim) > 64:
                self.prim.clear()
            v = gmpy2.primorial(L)
            self.prim[L] = v
        return v

    def phi(self, d, p):
        key = (d, p)
        v = self.cyc.get(key)
        if v is None:
            if len(self.cyc) > 200000:
                self.cyc.clear()
            v = mpz(p) ** d - 1
            for k in divisors(d)[:-1]:
                v //= self.phi(k, p)
            self.cyc[key] = v
        return v

    def fsig(self, p, e, L, known, slots):
        """σ(p^e)'nin çarpanları (dict) ya da None (buda). slots = boş yuva sayısı."""
        out = {}
        rest = []
        for d in divisors(e + 1)[1:]:
            m = self.phi(d, p)
            for r in list(known.keys()) + list(self.vT.keys()):
                if r == p:
                    continue
                if m % r == 0:
                    c = 0
                    while m % r == 0:
                        m //= r; c += 1
                    out[r] = out.get(r, 0) + c
            if m > 1:
                if self.odd and m % 2 == 0:
                    return None
                if gcd(m, self.primorial(L)) > 1:
                    return None
                rest.append(m)
        if not rest:
            return out
        if slots == 0:
            return None
        new = {}
        for m in rest:
            if is_prime(m):
                new[int(m)] = new.get(int(m), 0) + 1
                continue
            done = False
            for k in range(2, int(gmpy2.bit_length(m)) + 1):
                r, exact = iroot(m, k)
                if exact and is_prime(r):
                    new[int(r)] = new.get(int(r), 0) + k
                    done = True
                    break
            if done:
                continue
            if slots == 1 and len(new) >= 1:
                return None
            if slots == 1:
                return None   # m bileşik ve asal kuvveti değil ⇒ ≥ 2 yeni asal
            self.fallback += 1
            for r, v in factorint(int(m)).items():
                new[r] = new.get(r, 0) + v
        if len(new) > slots:
            return None
        for r, v in new.items():
            out[r] = out.get(r, 0) + v
        return out

    def force(self, L, known, k2):
        changed = True
        while changed:
            changed = False
            contrib = {}
            for p, (cls, emin, fx) in known.items():
                if fx is None:
                    continue
                f = self.fsig(p, fx, L, known, k2)
                if f is None:
                    return None
                for r, v in f.items():
                    contrib[r] = contrib.get(r, 0) + v
            for r, v in contrib.items():
                need = v - self.vT.get(r, 0)
                if r not in known:
                    if need <= 0:
                        continue
                    if r <= L or k2 == 0:
                        return None
                    if self.odd and r == 2:
                        return None
                    known = dict(known)
                    c = self.cls_of(r)
                    from engine_general import next_valid
                    known[r] = [c, next_valid(c, 1), None]
                    k2 -= 1
                    changed = True
                    break
                cls, emin, fx = known[r]
                if fx is not None:
                    if need > fx:
                        return None
                elif need > emin:
                    from engine_general import next_valid
                    ne = next_valid(cls, need)
                    if ne > self.emax:
                        self.unresolved.append(('emax', L, dict(known)))
                        return None
                    known = dict(known)
                    known[r] = [cls, ne, None]
                    changed = True
        return known, k2


if __name__ == '__main__':
    K = int(sys.argv[1]); T = int(sys.argv[2]); odd = sys.argv[3] == 'odd'
    emax = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    rep = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    E = Engine(K, T, odd, emax=emax, node_limit=10**9, report=rep).run()
    print(f"DONE K={K} T={T} {'odd' if odd else 'all'} nodes={E.nodes} maxL={E.maxL} maxe={E.maxe} "
          f"found={sorted(E.found)} unresolved={len(E.unresolved)} fallback={E.fallback} "
          f"t={time.time()-E.t0:.1f}s", flush=True)
    for u in E.unresolved[:20]:
        print(u)
