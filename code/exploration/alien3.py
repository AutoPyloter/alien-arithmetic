import numpy as np, math
from collections import Counter
N=10_000_000
s=np.ones(N+2,bool); s[:2]=False
for i in range(2,int((N+2)**.5)+1):
    if s[i]: s[i*i::i]=False
n=np.arange(N+2)
# Keşif A: yeni harf (asal) olma şansı, komşunun küçük harflerine göre
base=s[2:N].mean()
print("genel asal oranı",round(100*base,3))
for lab,m in [("a",2),("a.b",6),("a.b.c",30),("a.b.c.d",210),("a.b.c.d.e",2310)]:
    k=np.arange(m,N,m)
    nb=np.concatenate([k-1,k+1]); nb=nb[nb>1]
    print("komşusu",lab,"içeren:",round(100*s[nb].mean(),2),"%  kat:",round(s[nb].mean()/base,2))
# ikiz çiftler hangi sayının yanında
tw=np.nonzero(s[:N-1]&s[2:N+1])[0]  # p, p+2
mids=tw+1
print("ikiz sayısı",len(tw),"orta sayının a.b içerme oranı", round(100*np.mean(mids[mids>6]%6==0),2))
# Keşif B: Collatz'ı uzaylı gözüyle: tek n için 3n+1 kaç tane a içeriyor
odd=np.arange(1,2_000_001,2,dtype=np.int64)
v=3*odd+1
k=np.zeros_like(v)
t=v.copy()
while True:
    m=(t%2==0)
    if not m.any(): break
    k[m]+=1; t[m]//=2
c=Counter(k.tolist())
print("3n+1 içindeki a sayısı dağılımı:",{x:round(100*c[x]/len(k),2) for x in sorted(c)[:7]})
print("ortalama a sayısı",k.mean(),"-> adım başına çarpan 3/2^ort =",3/2**k.mean(), "log-ortalama", math.exp(math.log(3)-k.mean()*math.log(2)))
# gerçek Collatz: tek-adım sayısı ve küçülme
def steps(x):
    o=0;e=0
    while x!=1:
        if x%2: x=3*x+1;o+=1
        else: x//=2;e+=1
    return o,e
import random
random.seed(1)
r=[steps(random.randrange(10**11,10**12)) for _ in range(20000)]
ratio=np.mean([e/o for o,e in r if o])
print("gerçek yörüngelerde a-silme / b-ekleme oranı:",ratio)
# en uzun yörünge 1e6 altında
best=max(range(1,1_000_000),key=lambda x:sum(steps(x)))
print("1e6 altı en uzun:",best,steps(best))
