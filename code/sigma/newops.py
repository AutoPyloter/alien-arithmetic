import numpy as np, math, time
from sympy import Poly, symbols, primerange
X=symbols('X')
N=40_000
spf=np.zeros(N+2,dtype=np.int64)
for i in range(2,N+2):
    if spf[i]==0: spf[i::i]=np.where(spf[i::i]==0,i,spf[i::i])
PR=list(primerange(2,10**6)); IDX={p:i for i,p in enumerate(PR)}
from sympy import factorint
def vec(n):
    v={}
    if n>N+1:
        return {IDX[p]:e for p,e in factorint(n).items()}
    while n>1:
        p=int(spf[n]); v[IDX[p]]=v.get(IDX[p],0)+1; n//=p
    return v
def num(v):
    r=1
    for i,e in v.items(): r*=PR[i]**e
    return r
def sigma(n): return num({i+1:e for i,e in vec(n).items()})          # harf kaydırma a→b→c…
def star(n,m):                                                        # ⊛ : harf polinomlarını çarp
    u,w=vec(n),vec(m); r={}
    for i,e in u.items():
        for j,f in w.items(): r[i+j]=r.get(i+j,0)+e*f
    return num(r)
def dpar(n): return num({i-1:e*i for i,e in vec(n).items() if i>0})   # ∂ : polinom türevi
# yasaları doğrula
import random; random.seed(1); ok=[0,0,0,0]; T=3000
for _ in range(T):
    n,m,k=[random.randint(2,120) for _ in range(3)]
    ok[0]+= star(n,m*k)==star(n,m)*star(n,k)            # ⊛ çarpmaya dağılır
    ok[1]+= star(n,m)==star(m,n)                        # değişmeli
    ok[2]+= dpar(n*m)==dpar(n)*dpar(m)                  # ∂, ×'i korur (uzaylının toplaması)
    ok[3]+= dpar(star(n,m))==star(dpar(n),m)*star(n,dpar(m))  # Leibniz: ∂(n⊛m)=∂n⊛m × n⊛∂m
print("⊛ dağılma %d/%d, değişme %d/%d, ∂(×) %d/%d, Leibniz %d/%d"%(ok[0],T,ok[1],T,ok[2],T,ok[3],T))
print("örnekler: 6⊛6 =",star(6,6),"  σ(12) =",sigma(12),"  ∂(90) =",dpar(90),"  a⊛n=n? ",star(2,360)==360)
# ikinci düzey asallar: harf polinomu Z[X]'te indirgenemez (ve n tek harfin kuvveti değil gibi bayağı durumlar ayrı)
def poly(n): return Poly(sum(e*X**i for i,e in vec(n).items()),X)
t=time.time(); irr=np.zeros(N+1,bool)
for n in range(2,N+1):
    P=poly(n)
    c,fl=P.factor_list()
    tot=sum(e for _,e in fl)+ (sum(1 for _ in __import__('sympy').factorint(int(c)).values()) if c>1 else 0)
    irr[n]= tot==1 if c==1 else (len(fl)==0 and __import__('sympy').isprime(int(c)))
print("ikinci düzey asal (⊛-asal) sayısı ≤%d: %d  (süre %ds)"%(N,irr.sum(),time.time()-t))
for M in [10**3,10**4,4*10**4]: print("  ≤%d: %d  oran %.4f"%(M,irr[:M+1].sum(),irr[:M+1].mean()))
tw=np.nonzero(irr[2:N]&irr[3:N+1])[0]+2
print("⊛-asal komşu çiftleri (n, n+1) ≤%d: %d  ilk 12: %s"%(N,len(tw),tw[:12].tolist()))
np.save('irr2.npy',irr)
# σ ile + etkileşimi: σ(n+1)-σ(n)=2 ("σ-ikizleri")
c=[n for n in range(1,N) if sigma(n+1)-sigma(n)==2]
print("σ(n+1)=σ(n)+2 olan n ≤%d: %d tane: %s"%(N,len(c),c[:20]))
