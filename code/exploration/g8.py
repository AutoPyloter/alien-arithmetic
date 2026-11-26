import numpy as np, math, time, sys, json
from collections import defaultdict
N=int(sys.argv[1])
t=time.time()
rad=np.ones(N+1,dtype=np.int64)
isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]:
        isp[p*p::p]=False
        rad[p::p]*=p
print("rad elek",round(time.time()-t),flush=True)
# rad değerine göre gruplar (yalnız rad küçükler gerekecek)
maxK=int((N//(rad[1:].min()))) 
K=np.arange(N+1)//np.maximum(rad,1)
Kmax=int(K.max())
order=np.argsort(rad[1:],kind='stable')+1
rs=rad[order]
groups={}
cut=np.searchsorted(rs,Kmax)  # rad < Kmax
for n,r in zip(order[:cut].tolist(),rs[:cut].tolist()):
    groups.setdefault(r,[]).append(n)
for r in groups: groups[r].sort()
rkeys=sorted(groups)
print("gruplar",len(rkeys),round(time.time()-t),flush=True)
hits=[]
radl=rad
for c in range(3,N+1):
    rc=int(radl[c]); Kc=c//rc
    if Kc<2: continue
    # koşul: rad(a)*rad(b)*rc < c  => rad(a) < c/rc
    for r in rkeys:
        if r*rc>=c: break
        if math.gcd(r,rc)!=1: continue
        for a in groups[r]:
            if 2*a>c: break
            b=c-a
            rb=int(radl[b])
            if r*rb*rc<c and math.gcd(a,b)==1:
                hits.append((a,b,c,math.log(c)/math.log(r*rb*rc)))
print("bitti",round(time.time()-t),"isabet",len(hits),flush=True)
json.dump(hits,open('agents/g8_hits_%d.json'%N,'w'))
