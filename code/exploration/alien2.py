import numpy as np, math
from collections import Counter
N=10_000_000
# smallest prime factor sieve
spf=np.zeros(N+2,dtype=np.int32)
for i in range(2,N+2):
    if spf[i]==0:
        spf[i]=i
        if i*i<=N+1: 
            s=spf[i*i::i]; m=(s==0); s[m]=i; spf[i*i::i]=s
def fac(n):
    d={}
    while n>1:
        p=int(spf[n]); d[p]=d.get(p,0)+1; n//=p
    return d
isprime=(spf==np.arange(N+2))&(np.arange(N+2)>=2)
# 1 alphabet growth
print("== Alfabe büyümesi ==")
cp=np.cumsum(isprime)
for k in [10,100,1000,10**4,10**5,10**6,10**7]:
    print(k,int(cp[k]), round(k/math.log(k)))
# 2 omega distribution (letters count) via sieve
om=np.zeros(N+1,dtype=np.int8)
ps=np.nonzero(isprime[:N+1])[0]
for p in ps: om[p::p]+=1
print("== Harf sayısı dağılımı (n<=1e7) ==")
c=Counter(om[2:].tolist()); tot=N-1
for k in sorted(c): print(k, round(100*c[k]/tot,2))
print("ortalama",om[2:].mean(), "lnln N",math.log(math.log(N)))
# +1 transition: change in letters
d=om[3:N+1].astype(int)-om[2:N].astype(int)
print("== +1 harf değişimi ==",{k:round(100*v/len(d),1) for k,v in sorted(Counter(d.tolist()).items()) if abs(k)<=3})
# 4 Stormer: consecutive smooth pairs
def smooth(n,B):
    while n>1:
        if spf[n]>B: return False
        n//=int(spf[n])
    return True
for B,lab in [(3,"a,b"),(5,"a,b,c"),(7,"a-d"),(11,"a-e")]:
    pairs=[n for n in range(1,N) if smooth(n,B) and smooth(n+1,B)]
    print("== Sadece",lab,"harfli komşular:",len(pairs),"çift, en büyük:",pairs[-1],pairs[-1]+1)
# 3 powerful neighbors
def powerful(n):
    if n==1: return True
    return all(e>=2 for e in fac(n).values())
pw=[n for n in range(1,N) if powerful(n) and powerful(n+1)]
print("== Güçlü komşular:",pw[:12])
# 5 abc hits
def rad(n):
    r=1
    for p in fac(n): r*=p
    return r
hits=[]
M=20000
R=[0]+[rad(i) for i in range(1,M+1)]
for c_ in range(3,M+1):
    rc=R[c_]
    if rc*2>=c_: pass
    for a_ in range(1,c_//2+1):
        b_=c_-a_
        r=R[a_]*R[b_]*rc
        if r<c_ and math.gcd(a_,b_)==1:
            hits.append((math.log(c_)/math.log(r),a_,b_,c_))
hits.sort(reverse=True)
print("== abc isabetleri (c<=",M,"):",len(hits))
for h in hits[:6]: print(round(h[0],4),h[1:])
