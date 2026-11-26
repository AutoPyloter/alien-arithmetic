import numpy as np, math, time
TOP=10**9; S=10**7
r=math.isqrt(TOP+2)+1
sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
u=np.linspace(math.log(1e4),math.log(TOP),2**14); xs=np.floor(np.exp(u)).astype(np.int64)
cnt_tw=np.zeros(len(xs),np.int64); cnt_p=np.zeros(len(xs),np.int64)
tw_tot=0; p_tot=0; t=time.time()
for lo in range(0,TOP+1,S):
    hi=min(lo+S,TOP+1)
    seg=np.ones(hi-lo+2,bool)   # lo .. hi+1
    for p in ps:
        st=max(p*p,((lo+p-1)//p)*p)
        if st>hi+1: continue
        seg[st-lo::p]=False
    if lo==0: seg[0:2]=False
    isp=seg[:hi-lo]; twin=seg[:hi-lo]&seg[2:hi-lo+2]   # p in [lo,hi), p+2 prime (p+2<=hi+1)
    ctw=tw_tot+np.cumsum(twin); cp=p_tot+np.cumsum(isp)
    m=(xs>=lo)&(xs<hi)
    # ikiz sayımı: p+2<=x koşulu için p<=x-2
    idx=xs[m]-lo
    cnt_p[m]=cp[idx]
    j=idx-2; cnt_tw[m]=np.where(j>=0,ctw[np.maximum(j,0)],tw_tot)
    tw_tot=int(ctw[-1]); p_tot=int(cp[-1])
print("π(1e9)=",p_tot,"ikiz=",tw_tot," süre",round(time.time()-t))
np.save('tw9.npy',np.vstack([u,xs,cnt_tw,cnt_p]))
