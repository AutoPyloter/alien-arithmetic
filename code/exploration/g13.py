import numpy as np, math, time
TOP=10**9; S=10**7
r=math.isqrt(TOP)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
last=None; recs=[]; best=0; t=time.time()
for lo in range(0,TOP,S):
    hi=lo+S; seg=np.ones(S,bool)
    for p in ps:
        st=max(p*p,((lo+p-1)//p)*p)
        if st<hi: seg[st-lo::p]=False
    if lo==0: seg[:2]=False
    pr=np.nonzero(seg)[0]+lo
    if last is not None: pr=np.concatenate([[last],pr])
    g=np.diff(pr); i=np.argmax(g)
    if g[i]>best:
        # tüm yeni rekorlar
        for j in np.nonzero(g>best)[0]:
            if g[j]>best: best=int(g[j]); recs.append((int(pr[j]),best))
    last=int(pr[-1])
print("süre",round(time.time()-t))
print("p  boşluk  g/ln²p (Cramér oranı)")
for p,g in recs[-10:]: print(p,g,"%.3f"%(g/math.log(p)**2))
