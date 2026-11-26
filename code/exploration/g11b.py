import random
from fractions import Fraction as F
def u1_clean(L,e):
    L1,L2,L3=L; e1,e2,e3=e; K=sum(L)+sum(e); D=2**K-3**sum(L)
    N=(2**e1-1)*3**(L2+L3)+(2**e2-1)*2**(e1+L2)*3**L3+(2**e3-1)*2**(e1+e2+L2+L3)
    return F(N,D)
def check(L,e,u1):   # sistemi döndür
    u=u1
    for i in range(3):
        u=(3**L[i]*u+(2**e[i]-1))/F(2**(e[i]+L[(i+1)%3]))
    return u==u1
ok=all(check(L,e,u1_clean(L,e)) for L,e in [([random.randint(1,7) for _ in range(3)],[random.randint(1,7) for _ in range(3)]) for _ in range(200)] if 2**(sum(L)+sum(e))!=3**sum(L))
print("temiz u1 formülü 200 rastgele testte tutarlı:",ok)
