import sys, time
from fractions import Fraction as F
import engine_adaptive
from engine_adaptive import P2
from sympy import factorint
TH = int(sys.argv[3]); WEAK = sys.argv[4] == 'weak'
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
        if m>TH:
            self.skipped+=1; return out
        for r,v in factorint(m).items(): out[r]=out.get(r,0)+v
        new=[r for r in out if r not in known and r!=2]
        if len(new)>slots: return None
        return out
    def bounds(self, L, known, k2):
        if not WEAK: return super().bounds(L, known, k2)
        lo, hi, hik = super().bounds(L, known, 0)
        c = L + 1
        return lo, hik * F(c, c-1)**k2, hik
P2.ET = 16; P2.W = 2000
E = LL(int(sys.argv[1]), 2, True, emax=150, node_limit=int(sys.argv[2])); E.skipped = 0
t=time.time(); E.run()
print(sys.argv[1:], E.nodes, len(E.unresolved), E.skipped, E.maxL, round(time.time()-t,1), flush=True)
