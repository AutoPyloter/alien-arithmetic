import numpy as np, time
# 1) Brute force: bölen toplamı eleği, 1..N
N=50_000_000
t=time.time()
sig=np.zeros(N+1,dtype=np.int64)
for d in range(1,N//2+1):
    sig[2*d::d]+=d
perf=np.nonzero(sig[1:]==np.arange(1,N+1))[0]+1
print("Kaba kuvvetle 1..",N,":",perf.tolist(), f"({time.time()-t:.0f} sn)")
odd=sig[1::2]; n=np.arange(1,N+1,2)
print("Tek mükemmel sayı:", (odd==n).sum())
# en yakın tek 'neredeyse mükemmel' (bolluk oranı)
r=odd/n; i=np.argmax(r); print("En bol tek sayı:",n[i],"oran",r[i])
# 2) Euclid-Euler + Lucas-Lehmer
def isprime(p):
    if p<2: return False
    i=2
    while i*i<=p:
        if p%i==0: return False
        i+=1
    return True
def LL(p):
    if p==2: return True
    M=(1<<p)-1; s=4
    for _ in range(p-2): s=(s*s-2)%M
    return s==0
t=time.time(); res=[]
for p in range(2,4500):
    if isprime(p) and LL(p): res.append(p)
print("Mersenne üsleri:",res, f"({time.time()-t:.0f} sn)")
for k,p in enumerate(res[:8],1):
    print(k,p,(1<<(p-1))*((1<<p)-1))
for k,p in enumerate(res,1):
    if k>8:
        v=(1<<(p-1))*((1<<p)-1); print(k,p,"basamak:",len(str(v)))
