import numpy as np
N=20_000_000
P=np.load('/home/claude/P.npy'); P=P[P<=N]
Om=np.zeros(N+1,dtype=np.int8)  # harf sayısı (tekrarlarla) 
for p in P:
    pk=p
    while pk<=N:
        Om[pk::pk]+=1; pk*=p
lam=np.where(Om%2==0,1,-1).astype(np.int64); lam[0]=0
L=np.cumsum(lam[1:])
print("λ toplamı (çift harfli - tek harfli):")
for x in [10**3,10**4,10**5,10**6,10**7,2*10**7]: print(x,L[x-1], round(L[x-1]/x**.5,3))
print("pozitif olduğu ilk n>1:", 1+1+np.argmax(L[1:]>0) if (L[1:]>0).any() else None)
for h in [1,2,3,6]:
    c=np.mean(lam[1:N+1-h]*lam[1+h:N+1]); print("korelasyon λ(n)λ(n+%d):"%h, round(c,5))
# 3'lü desenler: 8 olası işaret deseni
w=lam[1:N-1]*4+lam[2:N]*2+lam[3:N+1]
u,c=np.unique(w,return_counts=True); print("3'lü desenler (beklenen %12.5):",[round(100*x/c.sum(),2) for x in c])
# Goldbach'ın parite versiyonu: n = p + q yerine n = (tek harf sayılı) + (tek harf sayılı) sayısı?
