import numpy as np, math, time, json
def segdata(lo,L):
    hi=lo+L+2; r=math.isqrt(hi)+1; sv=np.ones(r+1,bool); sv[:2]=False
    for i in range(2,math.isqrt(r)+1):
        if sv[i]: sv[i*i::i]=False
    ps=np.nonzero(sv)[0]
    n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); om=np.zeros(len(n),np.int8); spf=np.zeros(len(n),np.int64)
    for p in ps:
        st=(-lo)%p; z=spf[st::p]; z[z==0]=p; spf[st::p]=z
        pk=p
        while pk<hi:
            s2=(-lo)%pk; om[s2::pk]+=1; rem[s2::pk]//=p; pk*=p
    om+=(rem>1); spf[spf==0]=rem[spf==0]
    return spf,np.where(om%2==0,1,-1)
S=np.round(np.arange(0.10,0.505,0.025),3)
res={}
for X,L in [(10**7,10**7),(10**8,2*10**7),(10**9,2*10**7),(10**10,2*10**7)]:
    t=time.time(); spf,lam=segdata(X,L); lx=math.log(X+L/2)
    a=slice(0,L); b=slice(2,L+2); row=[]
    for s in S:
        z=math.exp(s*lx)
        pair=(spf[a]>z)&(spf[b]>z); one=spf[a]>z
        mm=np.mean((lam[a][pair]<0)&(lam[b][pair]<0)); p1=np.mean(lam[a][one]<0)
        row.append((float(s),float(mm),float(p1),int(pair.sum())))
    res[X]=row; print("X=%.0e bitti %ds"%(X,time.time()-t))
json.dump({str(k):v for k,v in res.items()},open('curve.json','w'))
