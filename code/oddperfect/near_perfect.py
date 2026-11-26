import numpy as np
N=10**7
s=np.zeros(N+1,dtype=np.int64)
for d in range(1,N+1):
    s[d::d]+=d
odd=np.arange(1,N+1,2)
r=s[odd]/odd
idx=np.argsort(np.abs(r-2))[:8]
def fac(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
for i in idx:
    n=int(odd[i]); print(n, s[n]-2*n, round(r[i],6), fac(n))
ab=odd[s[odd]>2*odd]; print("odd abundant count",len(ab),"first",ab[:5])
