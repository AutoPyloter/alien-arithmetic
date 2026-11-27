import sys, time
from engine_adaptive import P2
from sympy import primerange
import gmpy2
B = int(sys.argv[3])
PR = list(primerange(3, B + 1))
class LL(P2):
    def fsig(self, p, e, L, known, slots):
        N=(p**(e+1)-1)//(p-1); out={}; m=N
        for r in list(known)+[2]:
            if r==p: continue
            c=0
            while m%r==0: m//=r; c+=1
            if c: out[r]=c
        if m==1: return out
        if slots==0: return None
        t = None
        for r in PR:
            if r * r > m: break
            if m % r == 0: t = r; break
        if t is not None:
            if t <= L: return None
            c = 0; mm = m
            while mm % t == 0: mm //= t; c += 1
            out[t] = out.get(t,0)+c
            return out                        # tek asal eklenir, gerisi sonraki turda
        if m <= B*B:                          # m asal (B'ye kadar bölen yok)
            out[m] = 1; return out
        self.skipped += 1
        return out
P2.ET = int(sys.argv[4]); P2.W = 2000; P2.PB = int(sys.argv[5]) if len(sys.argv) > 5 else 0
E = LL(int(sys.argv[1]), 2, True, emax=150, node_limit=int(sys.argv[2])); E.skipped = 0
t=time.time(); E.run()
print(sys.argv[1:], E.nodes, len(E.unresolved), E.skipped, E.maxL, round(time.time()-t,1), flush=True)
