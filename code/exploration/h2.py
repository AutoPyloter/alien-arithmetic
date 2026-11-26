import numpy as np, math, random
P=np.load('/home/claude/P.npy'); N=10**8
s=np.zeros(N+1,bool); s[P]=True; cp=np.cumsum(s)
# H8: ⟨n⟩∩⟨n+k⟩ ⊆ ⟨k⟩  (test random)
random.seed(3); bad=0
for _ in range(200000):
    n=random.randrange(1,10**12); k=random.randrange(1,10**6)
    g=math.gcd(n,n+k)
    if k%g: bad+=1
print("H8 k-komşu yasası ihlali:",bad)
# H9: n² ile (n+1)² arasında en az 1 harf; H9': sayı / (n/ln n) oranı
mn=10**9; worst=None; rat=[]
for n in range(1,10000):
    c=cp[(n+1)**2]-cp[n*n]
    if c<mn: mn=c
    if n>10: rat.append((c/(n/math.log(n)),n))
print("H9 en az harf sayısı:",mn, " oran min/max (n>10):",min(rat),max(rat))
# H9'': [n, n+sqrt(n)] aralığında hep harf var mı? (daha güçlü)
fail=[n for n in range(2,10**7) if cp[n+int(math.isqrt(n))]-cp[n]==0]
print("H9'' [n, n+√n] boş kalanlar:",len(fail), fail[:10])
fail2=[n for n in range(2,10**7) if cp[n+int(0.5*math.isqrt(n))+1]-cp[n]==0]
print("H9''' [n, n+½√n] boş kalanlar:",len(fail2), fail2[-5:])
