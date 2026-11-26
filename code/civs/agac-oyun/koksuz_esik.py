"""Her k için: k köşeli köksüz ağaçların kanonik (en küçük) Matula numaralarının en büyüğü.
Tüm k-köşeli köksüz ağaçlar bu eşiğe kadar görünür. Karşılaştırma: köklü en büyük (A005518)."""
import sys; sys.path.insert(0,'/home/claude/civs/agac-oyun')
from functools import lru_cache
from matula import number, unrooted_canon
@lru_cache(maxsize=None)
def rooted(k):
    """k köşeli tüm köklü ağaçlar (kanonik tuple)."""
    if k == 1: return [()]
    out=set()
    def forests(m, maxc):   # m köşeli ormanlar, çocuklar azalmayan sırada
        if m==0: yield (); return
        for s in range(1, m+1):
            for c in rooted(s):
                if maxc is not None and (s, c) > maxc: continue
                for rest in forests(m-s, (s,c)):
                    yield rest + (c,)
    for f in forests(k-1, None): out.add(tuple(sorted(f)))
    return sorted(out)
A000081=[0,1,1,2,4,9,20,48,115,286,719,1842,4766,12486,32973]
for k in range(1,int(sys.argv[1]) if len(sys.argv)>1 else 13):
    R=rooted(k); assert len(R)==A000081[k]
    canon={unrooted_canon(t) for t in R}
    print(k, "köksüz:",len(canon), "en büyük kanonik:", max(canon), "köklü en büyük:", max(number(t) for t in R))
