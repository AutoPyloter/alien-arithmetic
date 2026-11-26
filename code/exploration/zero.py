import numpy as np, math
lam=np.load('/home/claude/lam.npy').astype(np.int64); N=10**8
L=np.cumsum(lam[1:N+1])
u=np.linspace(math.log(1e3),math.log(N),2**16)
x=np.exp(u).astype(np.int64)
g=L[x-1]/np.sqrt(x)
print("ortalama L/√x =",round(float(g.mean()),3)," 1/ζ(1/2)·? beklenen sabit ≈ 1/ζ(1/2) =",round(1/(-1.4603545),3))
g=g-g.mean(); w=np.hanning(len(g)); du=u[1]-u[0]
gam=np.linspace(1,40,3901)
# doğrudan Fourier (ln x ekseninde)
E=np.exp(-1j*np.outer(gam,u))
pw=np.abs(E@(g*w))*du
# tepe noktaları
pk=[i for i in range(1,len(gam)-1) if pw[i]>pw[i-1] and pw[i]>pw[i+1]]
pk=sorted(pk,key=lambda i:-pw[i])[:6]
for i in sorted(pk): print("tepe γ=%.2f güç=%.3f"%(gam[i],pw[i]))
# korelasyon tahmini
for r,gm in [(2,14.1347),(3,14.1347)]:
    print("cos(γ1·ln%d)=%.3f"%(r,math.cos(gm*math.log(r))))
