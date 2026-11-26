import numpy as np, random, math
from collections import Counter
# Collatz in alien form: odd->odd map T(n)= (3n+1)/2^k
def T(n):
    m=3*n+1; k=(m & -m).bit_length()-1; return m>>k,k
# A) ardışık k değerleri bağımsız mı? (k_i, k_{i+1}) korelasyonu
random.seed(7); ks=[]
for _ in range(3000):
    n=random.randrange(10**40,10**41)|1
    seq=[]
    for _ in range(60):
        n,k=T(n); seq.append(k)
    ks.append(seq)
a=np.array(ks)
x=a[:,:-1].ravel(); y=a[:,1:].ravel()
print("k ortalama",x.mean()," korelasyon(k_i,k_i+1)",round(np.corrcoef(x,y)[0,1],4))
print("P(k=1)",round(np.mean(x==1),4),"P(k_i+1=1|k_i=1)",round(np.mean(y[x==1]==1),4))
# B) n mod 2^m ilk m adımı belirler: kaç sınıf 'yükselir'?
for m in [4,8,12,16,20]:
    up=0
    for r in range(1,2**m,2):
        n=r; tot=0; steps=0; # simulate with symbolic: just use r + 2^m*big to avoid n small
        n=r+(2**m)*(10**30)
        logsum=0.0; used=0
        while used<m:
            n,k=T(n)
            if used+k>m: break
            used+=k; logsum+=math.log(3)-k*math.log(2)
        if logsum>0: up+=1
    print("mod 2^%d: tek sınıflar %d, ilk adımlarda net yükselen %%%.2f"%(m,2**(m-1),100*up/2**(m-1)))
# C) Rekor yükselişler: en uzun "şanssız seri" (ardışık k=1)
def run1(n):
    c=0
    while n%4==3: n,_=T(n); c+=1
    return c
print("2^k-1 sayıları ardışık k=1 serisi:",[(k,run1(2**k-1)) for k in [5,10,20,40]])
# D) 3n-1 ve 5n+1 varyantlarında döngü var mı (uzaylı: b yerine c eklersen?)
def cyc(a,b,lim=10**4,maxit=10**4):
    found=set()
    for s in range(1,lim):
        n=s; seen={}
        for i in range(maxit):
            if n in seen: found.add(min(n for n in list(seen)[seen[n]:])); break
            seen[n]=len(seen)
            n = n//2 if n%2==0 else a*n+b
            if n>10**15: break
    return sorted(found)
print("3n+1 döngüleri (min elemanlar):",cyc(3,1))
print("3n-1 döngüleri:",cyc(3,-1))
print("5n+1 döngüleri:",cyc(5,1))
