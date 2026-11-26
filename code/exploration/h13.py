from mpmath import mp, mpf, log, ceil, floor
mp.dps=80
a=log(3)/log(2); l2=log(2); l3=log(3)
V=mpf(2)**68
# 1) Küçük adaylar için kaba kontrol: 65/41
for K,L in [(2,1),(8,5),(65,41),(485,306),(24727,15601)]:
    d=K*l2-L*l3; print(K,L,"delta=%.3e"%float(d),"n_min <= %.4g"%float(L/(3*d)))
# 2) sürekli kesir + ara kesirler: "+" tarafı (K/L > log2 3) adaylar
cf=[]; x=a
for _ in range(40): t=int(floor(x)); cf.append(t); x=1/(x-t)
print("cf:",cf[:25])
h=[0,1]; k=[1,0]
cands=[]
for i,t in enumerate(cf):
    for j in range(1,t+1):            # ara kesirler dahil
        H=j*h[-1]+h[-2]; Kk=j*k[-1]+k[-2]
        if Kk>0 and H*l2-Kk*l3>0: cands.append((Kk,H))
    h.append(t*h[-1]+h[-2]); k.append(t*k[-1]+k[-2])
first=None
for L,K in sorted(set(cands)):
    d=K*l2-L*l3; b=L/(3*d)
    if b>=V:
        first=(L,K,float(b)); break
print("2^68'e kadar doğrulanmış varsayımıyla: bir döngü için gereken ilk aday L (tek adım sayısı), K:",first)
# kontrol: bu L'den küçük TÜM L için (K=ceil) bound < V mi? (en iyi yaklaşımlar zaten cf'de; teorem: en iyi tek yönlü yaklaşımlar ara kesirlerdir)
# Titiz kontrol: aday j ile j+1 arasındaki her L için δ_L >= δ_j  =>  bound <= (L_{j+1}-1)/(3 δ_j)
cs=sorted(set(cands)); worst=0; firstL=None
for (L1,K1),(L2,K2) in zip(cs,cs[1:]):
    d1=K1*l2-L1*l3
    if L1/(3*d1)>=V: firstL=L1; break
    worst=max(worst,float((L2-1)/(3*d1)))
    if (L2-1)/(3*d1)>=V:
        print("Ara bölgede risk: L",L1,"..",L2, "kaba sınır %.3g"%float((L2-1)/(3*d1))); firstL=('aralık',L1,L2); break
print("Titiz sonuç:",firstL)
L1=6586818670; K1=int(ceil(L1*a)); d1=K1*l2-L1*l3
print("K1",K1,"delta %.3e"%float(d1)," L alt sınırı:", int(ceil(3*V*d1)))
