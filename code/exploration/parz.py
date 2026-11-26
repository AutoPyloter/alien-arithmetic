import numpy as np, math, time
lo=900_000_000; L=50_000_000; hi=lo+L+2
r=math.isqrt(hi)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); om=np.zeros(len(n),np.int8)
spf=np.zeros(len(n),np.int64)   # en küçük harf
t=time.time()
for p in ps:
    st=(-lo)%p
    sl=slice(st,None,p)
    z=spf[sl]; z[z==0]=p; spf[sl]=z
    pk=p
    while pk<hi:
        s2=(-lo)%pk; om[s2::pk]+=1; rem[s2::pk]//=p; pk*=p
big=rem>1; om+=big; spf[spf==0]=rem[spf==0]
lam=np.where(om%2==0,1,-1)
print("elek süresi",round(time.time()-t))
a=slice(0,L); b=slice(2,L+2)
for z in [2,10,100,1000,10_000,30_000,math.isqrt(hi)]:
    surv=(spf[a]>z)&(spf[b]>z)
    la=lam[a][surv]; lb=lam[b][surv]; k=surv.sum()
    cls={"(-,-)":np.mean((la<0)&(lb<0)),"(-,+)":np.mean((la<0)&(lb>0)),"(+,-)":np.mean((la>0)&(lb<0)),"(+,+)":np.mean((la>0)&(lb>0))}
    print("z=%6d  hayatta kalan çift %9d   "%(z,k)+"  ".join("%s %.3f"%(c,v) for c,v in cls.items()))
