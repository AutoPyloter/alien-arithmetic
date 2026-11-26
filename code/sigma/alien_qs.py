import math, random, time
from sympy import nextprime, isprime, sqrt_mod
import numpy as np
random.seed(11)
def legendre(a,p): return pow(a%p,(p-1)//2,p)
def factor_alien(m, B, M):
    # harf tabanı: m'nin kare kalanı olduğu küçük harfler
    base=[2]+[p for p in range(3,B) if isprime(p) and legendre(m,p)==1]
    k=len(base); r=math.isqrt(m)+1
    # elek: Q(x)=(r+x)^2 - m, x in [0,M)
    xs=np.arange(M,dtype=object); Q=[(r+int(x))**2-m for x in range(M)]
    logs=np.array([math.log(q) for q in Q]); acc=np.zeros(M)
    for p in base:
        if p==2: 
            for x in range(M):
                if Q[x]%2==0: acc[x]+=math.log(2)
            continue
        for s in sqrt_mod(m,p,all_roots=True):
            st=(s-r)%p; acc[st::p]+=math.log(p)
    cand=np.nonzero(acc>logs-2.8*math.log(B))[0]
    rels=[]
    for x in cand:
        q=Q[x]; v=[]
        for p in base:
            e=0
            while q%p==0: q//=p; e+=1
            v.append(e)
        if q==1: rels.append((r+int(x),v))
        if len(rels)>k+10: break
    # mod 2 doğrusal cebir (uzaylı: harf üslerinin paritesi)
    rows=[sum(((e&1)<<i) for i,e in enumerate(v)) for _,v in rels]
    n=len(rows); hist=[1<<j for j in range(n)]
    piv={}
    for j in range(n):
        a=rows[j]; h=hist[j]
        while a:
            b=a.bit_length()-1
            if b in piv: pa,ph=piv[b]; a^=pa; h^=ph
            else: piv[b]=(a,h); break
        if a==0:
            idx=[i for i in range(n) if h>>i&1]
            X=1; ev=[0]*k
            for i in idx:
                X=X*rels[i][0]%m; ev=[a+b for a,b in zip(ev,rels[i][1])]
            Y=1
            for p,e in zip(base,ev): Y=Y*pow(p,e//2,m)%m
            g=math.gcd(X-Y,m)
            if 1<g<m: return g,len(base),len(rels)
    return None,len(base),len(rels)
for d,B,M in [(16,600,30000),(20,2000,300000),(24,4000,800000),(28,9000,2500000),(30,14000,4000000)]:
    p=nextprime(random.randrange(10**(d//2-1),10**(d//2))); q=nextprime(random.randrange(10**(d//2-1),10**(d//2))); m=p*q
    t=time.time(); g,kb,nr=factor_alien(m,B,M); dt=time.time()-t
    print("%2d basamak m=%d -> çarpan %s  (harf tabanı %d, ilişki %d, %.1f sn)"%(d,m,g,kb,nr,dt))
