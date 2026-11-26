import sympy as sp, sys, math
from functools import lru_cache
@lru_cache(None)
def nxt(p): return sp.nextprime(p)
def sig(n):
    r=1
    for p,e in sp.factorint(n).items(): r*=nxt(p)**e
    return r
def s(n): return sig(n)-n
res={}
for n0 in range(2,2001):
    n=n0; seen={n:0}; k=0; fate=None
    while k<200:
        n=s(n); k+=1
        if n==1: fate=('1',k); break
        if n in seen: fate=('döngü',k,k-seen[n],n); break
        seen[n]=k
        if n>10**40: fate=('patladı',k); break
    if fate is None: fate=('?',k,len(str(n)))
    res[n0]=fate
from collections import Counter
print(Counter(f[0] for f in res.values()))
cyc=Counter((f[2],f[3]) for f in res.values() if f[0]=='döngü')
print("döngüler:",list(cyc.items())[:20])
print("1'e gidenler:",[n for n,f in res.items() if f[0]=='1'][:30])
