import numpy as np, math
from scipy.optimize import linprog
from mpmath import mp, mpf, log, floor
c=math.log2(1.5)
def kappa(m):
    # değişkenler: L_0..L_{m-1}, x_0..x_{m-1}; minimize x_0
    nv=2*m; cost=np.zeros(nv); cost[m]=1
    Aub=[];bub=[]
    for k in range(m):
        r=np.zeros(nv); r[k]=1; r[m+k]=-1; Aub.append(r); bub.append(0)          # L_k - x_k <= 0
        r=np.zeros(nv); r[m+(k+1)%m]=1; r[k]=-c; r[m+k]=-1; Aub.append(r); bub.append(0)  # x_{k+1}-cL_k-x_k<=0
    Aeq=[np.r_[np.ones(m),np.zeros(m)]]; beq=[1]
    res=linprog(cost,A_ub=np.array(Aub),b_ub=bub,A_eq=np.array(Aeq),b_eq=beq,bounds=[(0,None)]*nv,method='highs')
    return res.fun, res.x[:m]
mp.dps=80
a=log(3)/log(2); l2=log(2); l3=log(3)
cf=[]; x=a
for _ in range(60): t=int(floor(x)); cf.append(t); x=1/(x-t)
h=[0,1]; k=[1,0]; cands=[]
for t in cf:
    for j in range(1,t+1):
        H=j*h[-1]+h[-2]; Kk=j*k[-1]+k[-2]
        if Kk>0 and H*l2-Kk*l3>0: cands.append((Kk,H))
    h.append(t*h[-1]+h[-2]); k.append(t*k[-1]+k[-2])
cands=sorted(set(cands))
def min_delta_upto(Lmax):
    best=None
    for L,K in cands:
        if L>Lmax: break
        best=K*l2-L*l3
    return best
V=mpf(2)**68
print(" m    κ(m)     L_max(LMN)     min δ_L (L≤L_max)   m/2^68     verifikasyonla kapanır mı")
for m in [40,50,60,68,75,80,91,100,120,150]:
    kap,Ls=kappa(m)
    Lmax=(11793.5+math.log(2*m))/(kap*math.log(2))
    # M=21 rejiminin geçerliliği: b'≈2.4427 L ≤ e^20.86
    for _ in range(60):
        M=max(math.log(2.4427*Lmax)+0.14,21); Lmax=(26.74*M*M+math.log(2*m))/(kap*math.log(2))
    md=min_delta_upto(Lmax)
    print("%4d  %.3e  %12.4g   %.3e        %.3e   %s"%(m,kap,Lmax,float(md),float(m/V),"EVET" if md>m/V else "HAYIR"))
print("κ(3) için en kötü L oranları:",np.round(kappa(3)[1],4))
