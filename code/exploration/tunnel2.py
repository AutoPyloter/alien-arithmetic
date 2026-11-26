import numpy as np, math, time
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
lo=10**9; L=12_000_000; hi=lo+L+6
r=math.isqrt(hi)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); Om=np.zeros(len(n),np.int8); om=np.zeros(len(n),np.int8); spf=np.zeros(len(n),np.int64)
for p in ps:
    st=(-lo)%p; om[st::p]+=1; z=spf[st::p]; z[z==0]=p; spf[st::p]=z
    pk=p
    while pk<hi:
        s2=(-lo)%pk; Om[s2::pk]+=1; rem[s2::pk]//=p; pk*=p
big=rem>1; Om+=big; om+=big; lpf=np.where(big,rem,spf); spf=np.where(spf==0,rem,spf)
isprime=(Om==1); lnN=np.log(n.astype(float))
idx=np.arange(0,L); rng=np.random.default_rng(0)
small=[3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
def run(zsieve,label,neighbors):
    surv=(n[idx]%2==1)
    for p in ps[ps<zsieve]: surv&=((n[idx]+2)%p!=0)
    sel=idx[surv]; y=isprime[sel+2].astype(int)
    H=np.stack([n[sel]%p for p in small],1).astype(float)
    feats=[]
    for k in neighbors:
        j=sel+k
        feats+= [Om[j],om[j],Om[j]%2,np.log(spf[j])/lnN[j],np.log(lpf[j])/lnN[j]]
    A=np.stack(feats,1).astype(float)
    perm=rng.permutation(len(y)); cut=int(0.7*len(y)); tr,te=perm[:cut],perm[cut:]
    out=[]
    for X,name in [(H,"İnsan"),(A,"Uzaylı"),(np.hstack([H,A]),"İnsan+Uzaylı")]:
        clf=HistGradientBoostingClassifier(max_iter=300,learning_rate=0.05,early_stopping=True,random_state=0).fit(X[tr],y[tr])
        p=clf.predict_proba(X[te])[:,1]; auc=roc_auc_score(y[te],p)
        bs=np.std([roc_auc_score(y[te][b],p[b]) for b in [rng.integers(0,len(te),len(te)) for _ in range(20)]])
        out.append("%s %.4f±%.4f"%(name,auc,bs))
    print("%-45s n=%d  asal oranı %.3f | %s"%(label,len(y),y.mean()," | ".join(out)))
run(30,"POZİTİF KONTROL (elek 30'a kadar), komşular n",[0])
run(1000,"elek 1000, uzaylı n'yi görüyor",[0])
run(1000,"elek 1000, uzaylı n,n+1,n+3,n+4'ü görüyor",[0,1,3,4])
