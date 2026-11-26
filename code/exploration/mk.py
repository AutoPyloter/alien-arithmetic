import sympy as sp, numpy as np, itertools, math, time
from scipy.linalg import eigh
from math import factorial
def partitions(n,k,maxp=None):
    if maxp is None: maxp=n
    if n==0: yield (); return
    if k==0: return
    for p in range(min(n,maxp),0,-1):
        for rest in partitions(n-p,k-1,p): yield (p,)+rest
def simplex_int(expo,k):  # ∫ over {t>=0, Σt<=1} ∏ t_i^{a_i}
    s=sum(expo); num=1
    for a in expo: num*=factorial(a)
    return sp.Rational(num,factorial(s+k))
def poly_int(P,vars_):
    k=len(vars_); tot=0
    for mon,c in sp.Poly(P,*vars_).terms(): tot+=c*simplex_int(mon,k)
    return tot
def Mk(k,d):
    t=sp.symbols('t1:%d'%(k+1))
    basis=[]
    for deg in range(d+1):
        for lam in partitions(deg,k):
            lam=lam+(0,)*(k-len(lam))
            perms=set(itertools.permutations(lam))
            basis.append(sp.Add(*[sp.Mul(*[t[i]**e for i,e in enumerate(pm)]) for pm in perms]))
    n=len(basis)
    I=np.zeros((n,n)); J=np.zeros((n,n))
    rest=t[:-1]; s=sum(rest)
    G=[sp.expand(sp.integrate(b,(t[-1],0,1-s))) for b in basis]
    for i in range(n):
        for j in range(i,n):
            I[i,j]=I[j,i]=float(poly_int(sp.expand(basis[i]*basis[j]),t))
            J[i,j]=J[j,i]=float(poly_int(sp.expand(G[i]*G[j]),rest)) if k>1 else 0
    w=eigh(J,I,eigvals_only=True)
    return k*w[-1], n
for k,d in [(2,8),(3,6),(4,5),(5,4),(6,3)]:
    t0=time.time(); m,n=Mk(k,d); print("k=%d derece≤%d taban=%d  M_k ≥ %.5f   (%.0fs)"%(k,d,n,m,time.time()-t0),flush=True)
# GPY tek boyutlu aile: F=(1-Σt)^a  ->  k(2a+2)(2a+1)/((a+1)^2(2a+k+1))
for k in [2,5,10,50,105,1000]:
    best=max(k*(2*a+2)*(2*a+1)/((a+1)**2*(2*a+k+1)) for a in np.linspace(0,200,4001))
    print("GPY ailesi k=%d: en iyi oran %.4f"%(k,best))
