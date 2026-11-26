"""Yeni gözlem testi: Matula ağaçlarında Yeşil Hackenbush P-pozisyonlarının (G=0) yoğunluğu."""
import numpy as np, collections, math
N = 10**7
spf = np.zeros(N+1, dtype=np.int32)
for i in range(2, int(N**.5)+1):
    if spf[i] == 0:
        blk = spf[i*i::i]; blk[blk == 0] = i
isp = (spf == 0); isp[:2] = False
spf[isp] = np.nonzero(isp)[0]
pidx = np.cumsum(isp).astype(np.int32)
spf = spf.tolist(); pidx = pidx.tolist()
G = [0]*(N+1); E=[0]*(N+1)
for n in range(2, N+1):
    p = spf[n]; G[n] = G[n//p] ^ (G[pidx[p]] + 1); E[n] = E[n//p] + E[pidx[p]] + 1
for x in (10**3,10**4,10**5,10**6,10**7):
    z = sum(1 for n in range(1,x+1) if G[n]==0)
    sq = math.isqrt(x)
    print(f"x={x:>9}: G=0 sayısı {z}, oran {z/x:.4f}, bunların kare olmayan {z-sq}")
# parite yasası G ≡ E (mod 2)
assert all((G[n]-E[n])%2==0 for n in range(1,N+1)); print("G ≡ kenar sayısı (mod 2): OK n<=1e7")
# değer dağılımı
c = collections.Counter(G[1:]); print("G değer dağılımı (ilk 12):", [(k,round(c[k]/N,4)) for k in range(12)])
# asallarda G hiç 0 değil; G(p)=G(pi(p))+1
# P-pozisyonu karesiz sayılar: ilk ~20
print("karesiz P-pozisyonları:", [n for n in range(2,400) if G[n]==0 and all(n%(q*q) for q in range(2,int(n**.5)+1))])
# G=0 oranı, E'ye göre (sabit kenar sayısında oran)
byE = collections.defaultdict(lambda:[0,0])
for n in range(1,N+1): byE[E[n]][0]+=1; byE[E[n]][1]+= (G[n]==0)
print("çift kenar sayısında G=0 oranı:", [(e, round(b/a,3)) for e,(a,b) in sorted(byE.items()) if e%2==0 and a>1000][:12])
