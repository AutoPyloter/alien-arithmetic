import math, numpy as np
from sympy import isprime
from fractions import Fraction
phi=(1+5**.5)/2
F=[1,2]
while F[-1]<10**15: F.append(F[-1]+F[-2])
def zeck_bits(n):
    out=0; k=len(F)-1; c=0
    while n:
        while F[k]>n: k-=1
        n-=F[k]; c+=1
    return c
# (e) tek harfli asallar: Fibonacci asalları
fp=[(i+2,f) for i,f in enumerate(F) if isprime(f)]
print("Fibonacci asalları (indeks, değer) ilk:", fp[:12])
# (f) asalların Zeckendorf rakam toplamı mod 2 ve mod 3
X=2_000_000
sieve=np.ones(X+1,bool); sieve[:2]=False
for i in range(2,int(X**.5)+1):
    if sieve[i]: sieve[i*i::i]=False
P=np.nonzero(sieve)[0]
s=np.array([zeck_bits(int(p)) for p in P])
print("asallar ≤2e6: Zeckendorf hane toplamı mod 2 = 0 oranı %.4f ; mod 3 dağılımı %s"%((s%2==0).mean(), np.round(np.bincount(s%3)/len(s),4)))
allz=np.array([zeck_bits(n) for n in range(1,X+1)])
print("tüm sayılar ≤2e6: mod 2 = 0 oranı %.4f"%((allz%2==0).mean()))
# (g) altın kaydırma s(n)=floor((n+1)phi)-1 ; p ve s(p) ikisi de asal
def sh(n):  # tam sayı ile: floor((n+1)*phi) = floor(((n+1)+sqrt(5)(n+1))/2)
    m=n+1; return (m+math.isqrt(5*m*m))//2 - 1
cnt=0; marks=[10**4,10**5,10**6,2*10**6]; mi=0; out=[]
for p in P:
    q=sh(int(p))
    if isprime(q): cnt+=1
    while mi<len(marks) and p>marks[mi]: out.append((marks[mi],cnt)); mi+=1
out.append((X,cnt))
for x,c in out: print("p ≤ %d: p ve kaydır(p) ikisi de asal: %d   (oran / (x/ln²x) = %.3f)"%(x,c,c/(x/math.log(x)**2)))
print("örnekler:", [(int(p),sh(int(p))) for p in P[:40] if isprime(sh(int(p)))][:10])
