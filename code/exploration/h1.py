import numpy as np, math
N=10_000_000
s=np.zeros(N+1,bool); P=np.load('/home/claude/P.npy'); P=P[P<=N]; s[P]=True
x=s.astype(np.int64)
# ---- H6: Goldbach yol sayısı ~ Hardy-Littlewood
C2=0.6601618158
def HL(n):
    f=1.0; m=n
    for p in P:
        if p*p>m: break
        if m%p==0:
            if p>2: f*=(p-1)/(p-2)
            while m%p==0: m//=p
    if m>2: f*=(m-1)/(m-2)
    # integral 2..n-2 of dt/(ln t ln(n-t)) numerik
    t=np.linspace(2,n-2,20001); I=np.trapezoid(1/(np.log(t)*np.log(n-t)),t)
    return 2*C2*f*I/2   # sırasız çift
def r(n):
    q=P[P<=n//2]; return int(np.sum(s[n-q]))
print("H6 Goldbach formülü:")
for n in [10**4,10**5,10**6,2*10**6+2,10**7-2,9699690]:
    print(n, r(n), round(HL(n),1), round(r(n)/HL(n),4))
# ---- H7: Goldbach'ta en küçük asal <= ln(n)^2 ?
M=2_000_000; worst=[]
best=0
for n in range(6,M+1,2):
    for p in P[1:]:
        if s[n-p]: break
    if p>best: best=p; worst.append((n,int(p)))
print("H7 rekorlar (n, en küçük p, ln²n, ln²n·lnln n):")
for n,p in worst[-6:]: print(n,p, round(math.log(n)**2), round(math.log(n)**2*math.log(math.log(n))))
