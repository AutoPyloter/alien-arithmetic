import numpy as np, math, time
TOP=10**9; S=10**7; HS=list(range(2,62,2)); MAXH=max(HS)
r=math.isqrt(TOP+MAXH)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
u=np.linspace(math.log(1e5),math.log(TOP),2**13); xs=np.floor(np.exp(u)).astype(np.int64)
C=np.zeros((len(HS)+1,len(xs)),np.int64); tot=np.zeros(len(HS)+1,np.int64); t=time.time()
for lo in range(0,TOP+1,S):
    hi=min(lo+S,TOP+1); seg=np.ones(hi-lo+MAXH,bool)
    for p in ps:
        st=max(p*p,((lo+p-1)//p)*p)
        if st<hi+MAXH: seg[st-lo::p]=False
    if lo==0: seg[:2]=False
    base=seg[:hi-lo]; m=(xs>=lo)&(xs<hi); idx=xs[m]-lo
    cs=tot[0]+np.cumsum(base); C[0,m]=cs[idx]; tot[0]=cs[-1]
    for k,h in enumerate(HS,1):
        pr=base&seg[h:h+hi-lo]; cs=tot[k]+np.cumsum(pr)
        j=idx-h; C[k,m]=np.where(j>=0,cs[np.maximum(j,0)],tot[k]); tot[k]=cs[-1]
print("bitti",round(time.time()-t),"sn; ikiz(1e9)=",tot[1]," π=",tot[0])
np.save('gaps.npy',C); np.save('gaps_u.npy',np.vstack([u,xs]))
