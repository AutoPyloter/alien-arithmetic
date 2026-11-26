import numpy as np, math, time
from collections import Counter
def segdata(lo,L):
    hi=lo+L+2; r=math.isqrt(hi)+1; sv=np.ones(r+1,bool); sv[:2]=False
    for i in range(2,math.isqrt(r)+1):
        if sv[i]: sv[i*i::i]=False
    ps=np.nonzero(sv)[0]
    n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); om=np.zeros(len(n),np.int8); spf=np.zeros(len(n),np.int64)
    for p in ps:
        st=(-lo)%p; z=spf[st::p]; z[z==0]=p; spf[st::p]=z
        pk=p
        while pk<hi:
            s2=(-lo)%pk; om[s2::pk]+=1; rem[s2::pk]//=p; pk*=p
    om+=(rem>1); spf[spf==0]=rem[spf==0]
    return spf,om
X,L=10**10,2*10**7
spf,om=segdata(X,L); a=slice(0,L); b=slice(2,L+2); lx=math.log(X)
for s in [0.1,0.2,0.25,1/3]:
    z=math.exp(s*lx); m=(spf[a]>z)&(spf[b]>z); A=om[a][m]; B=om[b][m]
    c=Counter(zip(A.tolist(),B.tolist())); tot=m.sum()
    top=sorted(c.items(),key=lambda kv:-kv[1])[:6]
    print("s=%.3f elekten geçen %d çift; en sık (Ω(n),Ω(n+2)):"%(s,tot)," ".join("%s:%.1f%%"%(k,100*v/tot) for k,v in top))
    print("      ikiz (1,1): %.2f%%   maks Ω: %d"%(100*c[(1,1)]/tot, max(A.max(),B.max())))
# ölçeklere göre Chen ve ikiz sayıları
print("\nölçek   ikiz(1,1)   Chen(1,≤2)   Chen/ikiz   Brun-tipi(≤2,≤2)")
for X,L in [(10**7,10**7),(10**8,10**7),(10**9,10**7),(10**10,10**7)]:
    spf,om=segdata(X,L); a=slice(0,L); b=slice(2,L+2); A=om[a]; B=om[b]
    tw=np.sum((A==1)&(B==1)); ch=np.sum((A==1)&(B<=2)); br=np.sum((A<=2)&(B<=2))
    print("1e%d   %8d   %9d   %7.2f    %9d"%(round(math.log10(X)),tw,ch,ch/tw,br))

# --- Selberg sahte dizi testi: n asal, n+2 asal (A) vs n+2 yarı-asal (B), s=1/3
X,L=10**10,2*10**7
spf,om=segdata(X,L); a=slice(0,L); b=slice(2,L+2); z=math.exp(math.log(X)/3)
n=np.arange(X,X+L,dtype=np.int64)
base=(om[a]==1)&(spf[b]>z)
A=n[base&(om[b]==1)]+2; B=n[base&(om[b]==2)]+2
print("\nA (n+2 asal): %d   B (n+2 iki büyük harfli): %d   A/(A+B)=%.3f  teori 1/(1+ln2)=%.3f"%(len(A),len(B),len(A)/(len(A)+len(B)),1/(1+math.log(2))))
rng=np.random.default_rng(0)
def tv(u,v,d):
    hu=np.bincount(u%d,minlength=d)/len(u); hv=np.bincount(v%d,minlength=d)/len(v); return 0.5*np.abs(hu-hv).sum()
print("mod d   TV(A,B)   TV(A yarısı, A yarısı) [gürültü]")
for d in [3,4,5,7,8,9,11,13,30,210,1001,2310]:
    perm=rng.permutation(len(A)); h=len(A)//2
    print("%5d   %.4f    %.4f"%(d,tv(A,B,d),tv(A[perm[:h]],A[perm[h:]],d)))
