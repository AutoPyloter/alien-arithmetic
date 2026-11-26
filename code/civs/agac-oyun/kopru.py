"""Köprü: Matula ağacı üzerinde Yeşil Hackenbush. Kök = yer.
Formül: G(1)=0, G(p_i)=G(i)+1, G(ab)=G(a) XOR G(b)  (Colon ilkesi).
Doğrudan oyun ağacıyla (mex) test edilir."""
import sys, time, collections; sys.path.insert(0,'/home/claude/civs/agac-oyun')
from functools import lru_cache
from matula import tree, number, G, V
from oyun import mex
from sympy import primepi, factorint, prime

def cuts(t):
    """t'den bir kenarı silince kalan (kökte bağlı) ağaçlar."""
    out = []
    for i, c in enumerate(t):
        rest = t[:i] + t[i+1:]
        out.append(rest)                       # kökteki kenarı kes
        for c2 in cuts(c):                     # daha derinde kes
            out.append(tuple(sorted(rest + (c2,))))
    return out

@lru_cache(maxsize=None)
def grundy_tree(t):
    return mex({grundy_tree(s) for s in cuts(t)})

if __name__ == "__main__":
    t0 = time.time(); M = 3000
    for n in range(1, M+1):
        assert grundy_tree(tree(n)) == G(n), n
    print(f"Yeşil Hackenbush = G(n) formülü, n<= {M}: OK ({time.time()-t0:.1f}s)")
    print("G(1..40):", [G(n) for n in range(1, 41)])
    # ikinci oyuncu kazanır (G=0) sayılar
    P = [n for n in range(1, 200) if G(n) == 0]
    print("G(n)=0 (P-pozisyonu):", P[:40])
    N = 200000
    print("G=0 yoğunluğu n<=",N, sum(G(n)==0 for n in range(1,N+1))/N)
    # G(n) <= E(n)=V(n)-1, eşitlik ne zaman?
    eqs=[n for n in range(1,300) if G(n)==V(n)-1]
    print("G(n)=kenar sayısı olanlar:", eqs[:30])
    # G ve sigma
    from matula import sigma
    print("G(sigma(n)) vs G(n) ilk 20:", [(G(n),G(sigma(n))) for n in range(1,21)])
