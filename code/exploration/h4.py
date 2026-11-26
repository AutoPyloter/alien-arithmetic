import numpy as np, math
from scipy.integrate import quad
P=np.load('/home/claude/P.npy'); s=np.zeros(10**8+3,bool); s[P]=True
C2=0.6601618158
for X in [10**4,10**6,10**8-2]:
    tw=int(np.sum(s[P[P<=X-2]+2]))
    pred=2*C2*quad(lambda t:1/math.log(t)**2,2,X,limit=200)[0]
    print("H12 ikiz",X,tw,round(pred),round(tw/pred,4))
def cyc(a,b,lim=3000):
    res={}
    for st in range(1,lim):
        n=st; seen=[]
        for _ in range(2000):
            if n in seen:
                c=seen[seen.index(n):]; key=min(c)
                L=sum(1 for v in c if v%2); K=len(c)-L
                res[key]=(K,L,len(c)); break
            seen.append(n); n=n//2 if n%2==0 else a*n+b
            if n>10**12: break
    return res
for a,b in [(5,1),(7,1),(3,-1),(5,-1),(3,1),(3,5),(3,7)]:
    r=cyc(a,b); print("H5' %dn%+d:"%(a,b),{k:(v[0],v[1],round(v[0]/v[1],3)) for k,v in r.items()}," log2(%d)=%.3f"%(a,math.log2(a)))
