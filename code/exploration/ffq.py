import numpy as np, itertools, math, sys, time
def run(q,n):
    # tüm monik polinomlar derece<=n: katsayı vektörleri (düşükten yükseğe), indeks = Σ c_i q^i (monik baş katsayı hariç)
    def allmonic(d):
        if d==0: return np.zeros((1,1),np.int64)+np.array([[1]])
        idx=np.arange(q**d)
        co=np.stack([(idx//q**i)%q for i in range(d)],1)
        return np.hstack([co,np.ones((len(idx),1),np.int64)])
    def enc(co):  # co: (k, d+1) monik
        d=co.shape[1]-1; return (co[:,:d]*(q**np.arange(d))).sum(1)
    def mul(P,G):  # P (d1+1,), G (k,d2+1)
        out=np.zeros((G.shape[0],len(P)+G.shape[1]-1),np.int64)
        for i,c in enumerate(P):
            if c: out[:,i:i+G.shape[1]]+=c*G
        return out%q
    # indirgenemezleri derece derece bul (elek)
    Om={d:np.zeros(q**d,np.int8) for d in range(n+1)}
    irr={}
    for d in range(1,n+1):
        # derece d'nin Ω'sı: daha küçük derecelerdeki indirgenemezlerin katları
        for e in range(1,d):
            for P in irr.get(e,[]):
                Pk=P.copy(); k=1
                while k*e<=d:
                    G=allmonic(d-k*e); f=mul(Pk,G); Om[d][enc(f)]+=1
                    k+=1
                    if k*e<=d: Pk=np.convolve(Pk,P)%q
        red=np.nonzero(Om[d]==0)[0]
        A=allmonic(d); irr[d]=[A[i] for i in red]
        Om[d][red]=1
    lam=np.where(Om[n]%2==0,1,-1)
    # f -> f+1 : sabit terim +1
    idx=np.arange(q**n); c0=idx%q; idx1=idx-c0+(c0+1)%q
    c=float((lam*lam[idx1]).mean())
    return c, len(irr[n])
res=[]
for q,n in [(3,4),(5,4),(7,4),(11,4),(13,4),(17,4),(19,4),(23,4),(3,5),(5,5),(7,5),(11,5),(13,5),(3,6),(5,6),(7,6)]:
    t=time.time(); c,ni=run(q,n)
    res.append((q,n,c)); print("q=%2d n=%d  λλ(f+1) ort=%+.5f  gürültü 1/√(q^n)=%.5f  Carmon–Rudnick ölçeği n/√q=%.3f  (%.0fs, indirgenemez %d)"%(q,n,c,q**(-n/2),n/math.sqrt(q),time.time()-t,ni),flush=True)
