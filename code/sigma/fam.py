import numpy as np, math, time, sys, json
from sympy import factorint, nextprime
P=np.load('P9.npy').astype(np.int64)
A,B=int(sys.argv[1]),int(sys.argv[2]); S=10**7; M1,M2=2147483647,2147483629
DS=[2,4,8,10,14,16,20,22,26,28,32,34,38,40,-2,-4,-8,-10]
small=P[P<=31623]; nxt=P[1:len(small)+1]
cand={d:[] for d in DS}; t=time.time()
for lo in range(A,B,S):
    hi=min(lo+S,B)+1
    n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); a1=np.ones(len(n),np.int64); a2=np.ones(len(n),np.int64)
    lim=math.isqrt(hi)+1
    for p,q in zip(small,nxt):
        if p>lim: break
        pk=int(p)
        while pk<hi:
            st=(-lo)%pk; sl=slice(st,None,pk); a1[sl]=a1[sl]*q%M1; a2[sl]=a2[sl]*q%M2; rem[sl]//=p; pk*=int(p)
    m=rem>1; qn=P[np.searchsorted(P,rem[m])+1]; a1[m]=a1[m]*(qn%M1)%M1; a2[m]=a2[m]*(qn%M2)%M2
    d1=(a1[1:]-a1[:-1])%M1; d2=(a2[1:]-a2[:-1])%M2
    for d in DS:
        c=np.nonzero((d1==d%M1)&(d2==d%M2))[0]
        cand[d]+= [int(lo+i) for i in c]
json.dump(cand,open('fam_%d.json'%A,'w')); print("bitti",round(time.time()-t),{d:len(v) for d,v in cand.items()})
