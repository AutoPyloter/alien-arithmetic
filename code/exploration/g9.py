import numpy as np, math, itertools
lam=np.load('/home/claude/lam.npy').astype(np.int8); N=10**8
x=N-20
rng=np.random.default_rng(0)
print("k  kaydırmalar            ortalama Π λ(n+h)     ×√N")
for k in range(2,7):
    for H in [tuple(range(k)), tuple([0,1,3,7,15,31][:k])]:
        prod=np.ones(x,np.int8)
        for h in H: prod=(prod*lam[1+h:x+1+h]).astype(np.int8)
        m=float(prod[:x].astype(np.int64).mean())
        print("%d  %-22s %+.6f   %+.2f"%(k,str(H),m,m*math.sqrt(x)))
