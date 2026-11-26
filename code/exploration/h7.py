import numpy as np, math
N=10**8
P=np.load('/home/claude/P.npy'); s=np.zeros(N+1,bool); s[P]=True
ev=np.arange(6,N+1,2,dtype=np.int64)
minp=np.zeros(len(ev),dtype=np.int64)
un=np.arange(len(ev))
for p in P[1:]:
    if len(un)==0: break
    hit=s[ev[un]-p]
    minp[un[hit]]=p; un=un[~hit]
# rekorlar
rec=[]; best=0
for i in np.nonzero(np.maximum.accumulate(minp)==minp)[0]:
    if minp[i]>best: best=minp[i]; rec.append((int(ev[i]),int(minp[i])))
print("rekor sayısı",len(rec))
for n,p in rec[-8:]:
    L=math.log(n); print(n,p, "p/ln²n=%.3f"%(p/L**2), "p/(ln²n·lnln n)=%.3f"%(p/(L**2*math.log(L))))
