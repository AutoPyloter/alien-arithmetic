import numpy as np, math, json
exec(open('/home/claude/curve.py').read().split("S=np.round")[0])   # segdata fonksiyonu
S=np.round(np.arange(0.20,0.505,0.05),3)
for X,L in [(10**8,2*10**7),(10**10,2*10**7)]:
    spf,lam=segdata(X,L+6); lx=math.log(X)
    a=slice(0,L); b=slice(2,L+2); c=slice(6,L+6)
    print("X=%.0e"%X)
    for s in S:
        z=math.exp(s*lx)
        m=(spf[a]>z)&(spf[b]>z)&(spf[c]>z); one=spf[a]>z
        mmm=np.mean((lam[a][m]<0)&(lam[b][m]<0)&(lam[c][m]<0)); p1=np.mean(lam[a][one]<0)
        print("  s=%.2f üçlü (○,○,○)=%.3f   P○³=%.3f   hayatta kalan %d"%(s,mmm,p1**3,m.sum()))
