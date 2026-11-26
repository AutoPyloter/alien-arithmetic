import numpy as np, math
lam=np.load('/home/claude/lam.npy').astype(np.int64); N=10**8
l=lam[1:N+1]
# A) blok iptali: [x,x+H] blok toplamları
print("H   RMS(blok)/√H   max|blok|/√H   rastgele beklenen max   %blok |ort|>0.1")
for H in [10,100,1000,10**4,10**5,10**6]:
    m=N//H; b=l[:m*H].reshape(m,H).sum(1)
    exp_max=math.sqrt(2*math.log(m))
    print(H, round(float(np.sqrt((b**2).mean())/math.sqrt(H)),3), round(float(np.abs(b).max()/math.sqrt(H)),2), round(exp_max,2), round(100*float(np.mean(np.abs(b)/H>0.1)),3))
# B) ayna yasası: λ(an)=-λ(n). L(x)/√x ile L(x/2)/√(x/2) ilişkisi
L=np.cumsum(l)
xs=np.unique(np.logspace(4,8,4000).astype(np.int64))
A=L[xs-1]/np.sqrt(xs); B=L[xs//2-1]/np.sqrt(xs//2); C=L[xs//3-1]/np.sqrt(xs//3)
print("korelasyon L(x)~L(x/2):",round(float(np.corrcoef(A,B)[0,1]),3)," L(x)~L(x/3):",round(float(np.corrcoef(A,C)[0,1]),3))
# C) spektrum: |Σ λ(n) e(nα)| / √N, ilk 2^24 sayı
M=2**24; F=np.abs(np.fft.rfft(l[:M].astype(np.float64)))/math.sqrt(M)
F[0]=0
idx=np.argsort(F)[-8:][::-1]
print("spektrum: rastgele beklenen max ≈",round(math.sqrt(math.log(M)),2))
for i in idx: print("  α=%.6f  güç=%.2f"%(i/M,F[i]))
