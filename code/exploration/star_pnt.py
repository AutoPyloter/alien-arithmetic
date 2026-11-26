import random, time, math, signal
from sympy import factorint, primepi, Poly, symbols, isprime
X=symbols('X')
class TO(Exception): pass
def h(s,f): raise TO()
signal.signal(signal.SIGALRM,h)
def irr(n):
    v=factorint(n)
    if 2 not in v and n!=3: return False       # teorem: a yoksa X böler
    P=Poly(sum(e*X**(int(primepi(p))-1) for p,e in v.items()),X)
    c,fl=P.factor_list()
    k=sum(e for _,e in fl)+(sum(factorint(int(c)).values()) if c>1 else 0)
    return k==1
random.seed(5)
# tam sayım küçük ölçekte
for M in [100,1000,5000]:
    print("≤%d: ⊛-asal sayısı %d, oran %.4f"%(M,sum(irr(n) for n in range(2,M+1)),sum(irr(n) for n in range(2,M+1))/(M-1)))
# örneklem büyük ölçekte (sadece çift sayılar aday; teorem)
for M in [10**4,10**5,10**6,10**7]:
    ok=tot=to=0; t=time.time()
    while tot<400 and time.time()-t<100:
        n=2*random.randint(M//20,M//2)
        signal.alarm(1)
        try: r=irr(n); tot+=1; ok+=r
        except TO: to+=1
        finally: signal.alarm(0)
    print("n≈%.0e (çiftler): ⊛-asal oranı %.3f ± %.3f  (örnek %d, zaman aşımı %d) → tüm sayılar için ≈ %.3f"%(M,ok/tot,math.sqrt(ok/tot*(1-ok/tot)/tot),tot,to,ok/tot/2))
