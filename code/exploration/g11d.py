import math
from mpmath import mp, mpf, log, floor
mp.dps=120
r=1/math.log2(3)
def kap(m): return r**(m-1)*(1-r)/(1-r**m)
a=log(3)/log(2); l2=log(2); l3=log(3)
cf=[]; x=a
for _ in range(90): t=int(floor(x)); cf.append(t); x=1/(x-t)
h=[0,1]; k=[1,0]; cands=[]
for t in cf:
    for j in range(1,t+1):
        H=j*h[-1]+h[-2]; Kk=j*k[-1]+k[-2]
        if Kk>0 and H*l2-Kk*l3>0: cands.append((Kk,H))
    h.append(t*h[-1]+h[-2]); k.append(t*k[-1]+k[-2])
cands=sorted(set(cands))
def first_L_with_delta_below(thr):
    for L,K in cands:
        if K*l2-L*l3<thr: return L
for X0e in [68,69,71]:
    V=mpf(2)**X0e; last=None
    for m in range(2,120):
        kp=kap(m); Lmax=1e4
        for _ in range(100):
            M=max(math.log(2.4427*Lmax)+0.14,21); Lmax=(26.74*M*M+math.log(2*m))/(kp*math.log(2))
        Lneed=first_L_with_delta_below(m/V)   # bir döngü için gereken en küçük L (verifikasyondan)
        ok=Lneed>Lmax
        if ok: last=(m,Lmax,int(Lneed))
        else: break
    print("X0=2^%d: yöntem m ≤ %d için kapanıyor (m=%d'de L_max=%.3g, gereken L ≥ %.3g); m=%d'de başarısız"%(X0e,last[0],last[0],last[1],last[2],m))
for m in [2,3,5,10,20,40,60]: print("κ(%d)=%.4e"%(m,kap(m)))
