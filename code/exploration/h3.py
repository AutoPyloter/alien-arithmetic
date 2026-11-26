import numpy as np, math, random
P=np.load('/home/claude/P.npy'); s=np.zeros(10**7+5000,bool); s[P[P<10**7+5000]]=True; cp=np.cumsum(s)
fail=[n for n in range(2,10**7) if cp[n+math.isqrt(n)]-cp[n]==0]; print("H9'' son istisna:",fail[-1])
def traj(n):
    peak=n; st=0; m=n
    while m!=1:
        m = m//2 if m%2==0 else 3*m+1
        st+=1
        if m>peak: peak=m
    return st,peak
# H10: tepe <= n^2 ?
recs=[]; best=0
for n in range(3,300000,2):
    st,pk=traj(n); e=math.log(pk)/math.log(n)
    if e>best: best=e; recs.append((n,pk,round(e,3)))
print("H10 tepe üssü rekorları:",recs[-6:])
# H11: toplam adım ≈ 10.43·ln n  (yazı-tura modeli tahmini 3/ln(4/3))
pred=3/math.log(4/3); print("model katsayısı",round(pred,3))
random.seed(5)
for d in [6,12,24,48,96]:
    xs=[random.randrange(10**d,10**(d+1)) for _ in range(3000)]
    v=[traj(x)[0]/math.log(x) for x in xs]
    print("10^%d: adım/ln n ortalama %.3f  std %.3f"%(d,np.mean(v),np.std(v)))
