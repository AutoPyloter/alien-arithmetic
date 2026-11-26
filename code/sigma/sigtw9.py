import numpy as np, math, time
from sympy import factorint, nextprime
P=np.load('P9.npy').astype(np.int64)
import sys; A,B=int(sys.argv[1]),int(sys.argv[2]); TOP=B; S=10**7; M1,M2=2147483647,2147483629
small=P[P<=31623]; nxt_small=P[1:len(small)+1]
found=[]; t=time.time(); prev=None
hist_lo=np.zeros(201,np.int64)   # D(n)/n histogramı (-1..1, 0.01 adım) n>10^6
for lo in range(A,TOP+1,S):
    hi=min(lo+S,TOP+1)+1
    n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); a1=np.ones(len(n),np.int64); a2=np.ones(len(n),np.int64)
    for p,q in zip(small,nxt_small):
        pk=int(p)
        while pk<hi:
            st=(-lo)%pk; sl=slice(st,None,pk)
            a1[sl]=a1[sl]*q%M1; a2[sl]=a2[sl]*q%M2; rem[sl]//=p; pk*=int(p)
    m=rem>1
    qn=P[np.searchsorted(P,rem[m])+1]
    a1[m]=a1[m]*(qn%M1)%M1; a2[m]=a2[m]*(qn%M2)%M2
    d1=(a1[1:]-a1[:-1]-2)%M1; d2=(a2[1:]-a2[:-1]-2)%M2
    c=np.nonzero((d1==0)&(d2==0))[0]
    found+= [int(lo+i) for i in c]
print("aday:",len(found)," süre",round(time.time()-t))
PR={}
def sig(x):
    r=1
    for p,e in factorint(x).items(): r*=int(nextprime(p))**e
    return r
ok=[x for x in found if sig(x+1)-sig(x)==2]
print("doğrulanmış σ-ikizleri ≤10^8:",len(ok)); print(ok)
np.save('sigtw_%d.npy'%A,np.array(ok))
