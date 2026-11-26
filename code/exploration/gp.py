import numpy as np, math
TOP=10**9+200; S=10**7
r=math.isqrt(TOP)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]; out=[]
for lo in range(0,TOP,S):
    hi=min(lo+S,TOP); seg=np.ones(hi-lo,bool)
    for p in ps:
        st=max(p*p,((lo+p-1)//p)*p)
        if st<hi: seg[st-lo::p]=False
    if lo==0: seg[:2]=False
    out.append((np.nonzero(seg)[0]+lo).astype(np.uint32))
P9=np.concatenate(out); np.save('P9.npy',P9); print(len(P9),P9[-1])
