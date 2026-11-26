import sympy as sp, sys
from functools import lru_cache
@lru_cache(None)
def nxt(p): return sp.nextprime(p)
def sig(n):
    r=1
    for p,e in sp.factorint(n).items(): r*=nxt(p)**e
    return r
N=int(sys.argv[1]); fate={1:('1',None)}
cycles=set(); maxpeak=(0,0); maxlen=(0,0)
for n0 in range(2,N+1):
    path=[]; pos={}; n=n0; peak=n0
    while n not in fate and n not in pos:
        pos[n]=len(path); path.append(n); n=sig(n)-n; peak=max(peak,n)
        if len(path)>2000: break
    if n in pos:  # new cycle
        cyc=tuple(path[pos[n]:]); m=min(cyc); i=cyc.index(m); cyc=cyc[i:]+cyc[:i]
        cycles.add(cyc); f=('döngü',cyc)
    elif n in fate: f=fate[n]
    else: f=('?',None)
    for x in path: fate[x]=f
    if peak>maxpeak[0]: maxpeak=(peak,n0)
    if len(path)>maxlen[0]: maxlen=(len(path),n0)
from collections import Counter
c=Counter(fate[n][0] for n in range(2,N+1)); print(N,c)
for cy in sorted(cycles): print(len(cy),cy, sum(1 for n in range(2,N+1) if fate[n][1]==cy))
print("en yüksek tepe",maxpeak,"en uzun yol",maxlen)
