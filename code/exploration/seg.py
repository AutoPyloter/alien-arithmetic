import numpy as np, math, time
TOP=907_000_000; S=10_000_000
r=math.isqrt(TOP)+1
sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0].astype(np.int64)
total=0; t=time.time(); found=None
for lo in range(1,TOP+1,S):
    hi=min(lo+S,TOP+1); n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); om=np.zeros(hi-lo,np.int8)
    for p in ps:
        pk=p
        while pk<hi:
            st=(-lo)%pk
            om[st::pk]+=1; rem[st::pk]//=p
            pk*=p
    om+= (rem>1)
    lam=np.where(om%2==0,1,-1).astype(np.int64)
    if lo==1: lam[0]=1
    cs=total+np.cumsum(lam)
    if found is None and lo>2:
        pos=np.nonzero(cs>0)[0]
        if len(pos): found=(int(n[pos[0]]),int(cs[pos[0]]))
    total=int(cs[-1])
print("L(%d)=%d"%(TOP,total)," ilk pozitif:",found, " süre",round(time.time()-t))
