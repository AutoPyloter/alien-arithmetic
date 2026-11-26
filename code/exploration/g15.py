import math, time
import numpy as np
# deterministik Miller-Rabin (n < 3.3e24)
def isp(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x==1 or x==n-1: continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
# Bateman–Horn sabiti n²+1: C = 1/2 ∏_{p>2} (1 - χ(p)/(p-1)), χ(p)=(-1/p)
P=[p for p in range(3,2_000_000) if all(p%q for q in (2,3,5,7)) or p in (3,5,7)]
sv=np.ones(2_000_001,bool); sv[:2]=False
for i in range(2,1415):
    if sv[i]: sv[i*i::i]=False
PR=np.nonzero(sv)[0]; PR=PR[PR>2]
chi=np.where(PR%4==1,1,-1)
C=0.5*np.prod(1-chi/(PR-1.0))
print("Bateman–Horn sabiti (p<2·10^6 çarpımı) C ≈ %.5f"%C)
t=time.time(); cnt=0; marks=[10**3,10**4,10**5,10**6]; res=[]
for n in range(1,10**6+1):
    if isp(n*n+1): cnt+=1
    if n in marks:
        I=sum(1/math.log(k*k+1) for k in range(2,n+1))
        res.append((n,cnt,C*I))
print("süre",round(time.time()-t))
for n,c,pr in res: print("n≤%d: n²+1 asal sayısı %d   tahmin %.0f   oran %.4f"%(n,c,pr,c/pr))
