import numpy as np, math
N=10**8
P=np.load('/home/claude/P.npy')
Om=np.zeros(N+1,dtype=np.int8)
for p in P:
    pk=int(p)
    while pk<=N:
        Om[pk::pk]+=1; pk*=int(p)
lam=np.where(Om%2==0,1,-1).astype(np.int8); lam[0]=0
np.save('/home/claude/lam.npy',lam)
L=np.cumsum(lam[1:],dtype=np.int64)
# 1) kesin yasa: sum_{n<=x} λ(n)*floor(x/n) = floor(sqrt x)
for x in [10,1000,123456,10**6]:
    n=np.arange(1,x+1); v=int(np.sum(lam[1:x+1].astype(np.int64)*(x//n)))
    print("yasa x=%d: %d vs √x=%d"%(x,v,math.isqrt(x)))
# 2) koşullu korelasyon λ(n)λ(n+1), n mod 30 sınıflarına göre (n<=1e8)
pr=lam[1:N].astype(np.int64)*lam[2:N+1]
n=np.arange(1,N)
res={r:round(float(pr[n%30==r].mean()),4) for r in range(30)}
print("mod30 koşullu korelasyon min/max:",min(res.values()),max(res.values()))
# 3) asal komşuların rengi: λ(p-1), λ(p+1)
q=P[(P>2)&(P<N)]
print("ort λ(p-1):",round(float(lam[q-1].mean()),5)," ort λ(p+1):",round(float(lam[q+1].mean()),5), " (asal sayısı",len(q),")")
for X in [10**4,10**6,10**8]:
    qq=q[q<X]; print("  X=%d  Σλ(p-1)=%d  √π(X)=%d"%(X,int(lam[qq-1].astype(np.int64).sum()),int(math.sqrt(len(qq)))))
# 4) Chowla: düz ve logaritmik ortalama
w=1.0/n
for X in [10**4,10**6,10**8-1]:
    a=pr[:X-1].mean(); b=float(np.sum(pr[:X-1]*w[:X-1])/np.sum(w[:X-1]))
    print("Chowla X=%d düz=%.5f log=%.5f"%(X,a,b))
# 5) renk yürüyüşü L(x)/√x
r=L/np.sqrt(np.arange(1,N+1))
for X in [10**3,10**5,10**6,10**7,10**8]:
    print("X=%d  L=%d  max|L|/√x (x<=X)=%.3f"%(X,L[X-1],np.abs(r[10:X]).max()))
print("ilk pozitif L (x>1):", int(np.argmax(L[1:]>0))+2 if (L[1:]>0).any() else "yok (≤1e8)")
