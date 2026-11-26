import numpy as np, math, time
TOP=10**9; S=10**7; PAD=4000
r=math.isqrt(TOP)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]; small=ps[1:600]   # 3.. ~4400
best=0; rec=[]; t=time.time()
for lo in range(0,TOP,S):
    a=max(lo-PAD,0); hi=lo+S
    seg=np.ones(hi-a,bool)
    for p in ps:
        st=max(p*p,((a+p-1)//p)*p)
        if st<hi: seg[st-a::p]=False
    if a==0: seg[:2]=False
    ev=np.arange(max(lo,6)+(max(lo,6)%2),hi,2,dtype=np.int64)
    un=np.arange(len(ev)); mp=np.zeros(len(ev),np.int64)
    for p in small:
        if len(un)==0: break
        h=seg[ev[un]-p-a]; mp[un[h]]=p; un=un[~h]
    if len(un): print("ÇÖZÜLEMEDİ!",ev[un][:5]); break
    mx=mp.max()
    if mx>best:
        cm=np.maximum.accumulate(mp); 
        for i in np.nonzero((cm==mp)&(mp>best))[0]:
            if mp[i]>best: best=int(mp[i]); rec.append((int(ev[i]),best))
print("süre",round(time.time()-t))
for n,p in rec[-10:]:
    Ln=math.log(n); print(n,p,"p/ln²n=%.3f  p/(ln²n lnln n)=%.3f"%(p/Ln**2,p/(Ln**2*math.log(Ln))))
