import numpy as np, math, time
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, log_loss
lo=10**9; L=30_000_000; hi=lo+L+3
r=math.isqrt(hi)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
n=np.arange(lo,hi,dtype=np.int64); rem=n.copy()
Om=np.zeros(len(n),np.int8); om=np.zeros(len(n),np.int8); spf=np.zeros(len(n),np.int64); sq=np.zeros(len(n),np.int8)
t=time.time()
for p in ps:
    st=(-lo)%p; om[st::p]+=1
    z=spf[st::p]; z[z==0]=p; spf[st::p]=z
    pk=p; e=0
    while pk<hi:
        s2=(-lo)%pk; Om[s2::pk]+=1; rem[s2::pk]//=p
        if e>=1: sq[s2::pk]=np.maximum(sq[s2::pk],1)
        pk*=p; e+=1
big=rem>1; Om+=big; om+=big
lpf=np.where(big,rem,0)  # en büyük harf (büyük kalan varsa)
# lpf yoksa: en büyük küçük asal; yaklaşık olarak spf ile doldur (nadir durum)
lpf=np.where(lpf==0,spf,lpf); spf=np.where(spf==0,rem,spf)
isprime=(Om==1)
print("elek",round(time.time()-t),"sn")
idx=np.arange(0,L,1)
m_odd=(n[idx]%2==1)
# n+2 1000'e kadar elekten geçmiş olsun
surv=np.ones(L,bool)
for p in ps[ps<1000]: surv&= ((n[idx]+2)%p!=0)
sel=idx[m_odd&surv]
y=isprime[sel+2].astype(int)
N=n[sel].astype(float); lnN=np.log(N)
# İNSAN özellikleri: n'nin küçük asallara göre kalanları (3..97)
small=[3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
H=np.stack([n[sel]%p for p in small],1).astype(float)
# UZAYLI özellikleri: n'nin çarpanlara ayrılışı
A=np.stack([Om[sel],om[sel],(Om[sel]%2),sq[sel],np.log(spf[sel])/lnN,np.log(lpf[sel])/lnN,isprime[sel].astype(int)],1).astype(float)
print("örnek sayısı",len(y)," n+2 asal oranı %.3f"%y.mean())
rng=np.random.default_rng(0); perm=rng.permutation(len(y)); cut=int(0.7*len(y))
tr,te=perm[:cut],perm[cut:]
def fit(X,name):
    clf=HistGradientBoostingClassifier(max_iter=300,learning_rate=0.05,max_leaf_nodes=31,early_stopping=True,random_state=0)
    clf.fit(X[tr],y[tr]); p=clf.predict_proba(X[te])[:,1]
    auc=roc_auc_score(y[te],p); ll=log_loss(y[te],p)
    # bootstrap AUC
    bs=[roc_auc_score(y[te][b],p[b]) for b in [rng.integers(0,len(te),len(te)) for _ in range(30)]]
    print("%-28s AUC=%.4f ± %.4f   log-kayıp=%.5f"%(name,auc,np.std(bs),ll)); return p
p0=np.full(len(te),y[tr].mean()); print("%-28s log-kayıp=%.5f"%("taban (sabit oran)",log_loss(y[te],p0)))
pH=fit(H,"İnsan (kalanlar)")
pA=fit(A,"Uzaylı (çarpanlar)")
pHA=fit(np.hstack([H,A]),"İnsan + Uzaylı")
np.save('tunnel_data.npy',np.hstack([H,A,y[:,None]]))
