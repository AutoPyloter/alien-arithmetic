import numpy as np, math
lam=np.load('/home/claude/lam.npy').astype(np.float64)
print("x   Σλ(n)/n·x   E(x)=Σλ(n){x/n}   E/√x")
for x in [10**3,10**4,10**5,10**6,10**7,3*10**7]:
    n=np.arange(1,x+1,dtype=np.float64); l=lam[1:x+1]
    fr=(x/n)-np.floor(x/n)
    S=float(np.sum(l/n))*x; E=float(np.sum(l*fr))
    print(x, round(S,2), round(E,2), round(E/math.sqrt(x),3))
