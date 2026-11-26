import numpy as np, math, time, sys, json
def run(q,N):
    t0=time.time()
    Om=[None]+[np.zeros(q**n,np.int8) for n in range(1,N+1)]   # Om[n][idx]
    def coeffs(n):  # tüm monik derece-n polinomların katsayıları (q^n x (n+1)), son katsayı 1
        idx=np.arange(q**n,dtype=np.int64); C=np.zeros((q**n,n+1),np.int64)
        for i in range(n): C[:,i]=(idx//q**i)%q
        C[:,n]=1; return C
    def encode(C,n):  # monik derece n
        v=np.zeros(len(C),np.int64)
        for i in range(n): v+=C[:,i]*q**i
        return v
    def mul_all(Pc,m):  # P * tüm monik derece m
        G=coeffs(m) if m>0 else np.ones((1,1),np.int64)
        d=len(Pc)-1; R=np.zeros((len(G),d+m+1),np.int64)
        for i,c in enumerate(Pc):
            if c: R[:,i:i+m+1]+=c*G
        return R%q
    irr_count={}
    for d in range(1,N+1):
        Cd=coeffs(d); irr=np.nonzero(Om[d]==0)[0]; irr_count[d]=len(irr)
        for ix in irr:
            P=Cd[ix].copy(); Pk=P.copy(); k=1
            while (len(Pk)-1)<=N:
                dk=len(Pk)-1
                for m in range(0,N-dk+1):
                    R=mul_all(Pk,m); Om[dk+m][encode(R,dk+m)]+=1
                # Pk*=P
                newk=np.zeros(len(Pk)+d,np.int64)
                for i,c in enumerate(P):
                    if c: newk[i:i+len(Pk)]+=c*Pk
                Pk=newk%q; k+=1
    return Om,irr_count,time.time()-t0
def Sq(q,h_is_t,D=200):
    # Π_P (1-1/|P|)^-2 (1-1/|P| - 1_{P∤h}/|P|); |P|=q^d; irreducible sayısı Möbius formülü
    def mu(n):
        r=1;m=n;p=2
        while p*p<=m:
            if m%p==0:
                m//=p
                if m%p==0: return 0
                r=-r
            p+=1
        return -r if m>1 else r
    S=1.0
    for d in range(1,D+1):
        I=sum(mu(d//e)*q**e for e in range(1,d+1) if d%e==0)//d
        x=q**(-d)
        f=(1-2*x)/(1-x)**2
        if h_is_t and d==1:
            S*=f**(I-1)*(1/(1-x))
        else: S*=f**I
    return S
res={}
for q,N in [(3,12),(5,8),(7,7),(2,16)]:
    Om,ic,tt=run(q,N); print("q=%d N=%d süre %.0fs"%(q,N,tt),flush=True)
    rows=[]
    S1=Sq(q,False); St=Sq(q,True)
    for n in range(1,N+1):
        isp=(Om[n]==1); idx=np.arange(q**n)
        c0=idx%q; f1=idx-c0+((c0+1)%q)   # f+1
        tw1=int(np.sum(isp & isp[f1]))
        if n>=2:
            c1=(idx//q)%q; ft=idx-c1*q+((c1+1)%q)*q
            twt=int(np.sum(isp&isp[ft]))
        else: twt=None
        lam=np.where(Om[n]%2==0,1,-1)
        corr=float(np.mean(lam*lam[f1])); Lsum=int(lam.sum())
        Lth= q**(n//2) if n%2==0 else -q**((n+1)//2)
        rows.append(dict(n=n,irr=int(isp.sum()),pnt=q**n/n,tw1=tw1,pred1=S1*q**n/n**2,twt=twt,predt=St*q**n/n**2 if n>=2 else None,corr=corr,L=Lsum,Lth=Lth))
    res[q]=dict(rows=rows,S1=S1,St=St)
    for r in rows: print(r,flush=True)
json.dump({str(k):v for k,v in res.items()},open('agents/g3.json','w'))
