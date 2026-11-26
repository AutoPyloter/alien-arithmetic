import numpy as np, math, time
TOP=10**9; S=10**7
r=math.isqrt(TOP)+1; sv=np.ones(r+1,bool); sv[:2]=False
for i in range(2,math.isqrt(r)+1):
    if sv[i]: sv[i*i::i]=False
ps=np.nonzero(sv)[0]
u=np.linspace(math.log(1e3),math.log(TOP),2**15); xs=np.floor(np.exp(u)).astype(np.int64)
Lx=np.zeros(len(xs),np.int64); tot=0; t=time.time()
for lo in range(1,TOP+1,S):
    hi=min(lo+S,TOP+1); n=np.arange(lo,hi,dtype=np.int64); rem=n.copy(); om=np.zeros(hi-lo,np.int8)
    for p in ps:
        pk=p
        while pk<hi:
            st=(-lo)%pk; om[st::pk]+=1; rem[st::pk]//=p; pk*=p
    om+=(rem>1)
    lam=np.where(om%2==0,1,-1).astype(np.int64)
    cs=tot+np.cumsum(lam); m=(xs>=lo)&(xs<hi); Lx[m]=cs[xs[m]-lo]; tot=int(cs[-1])
print("L(1e9)=",tot," süre",round(time.time()-t))
np.save('/home/claude/L1e9.npy',np.vstack([u,xs,Lx]))
g=Lx/np.sqrt(xs); print("ort L/√x=%.4f (1/ζ(1/2)=-0.6848), max|L|/√x=%.3f"%(g.mean(),np.abs(g[100:]).max()))
g=g-g.mean(); w=np.hanning(len(g)); du=u[1]-u[0]
gam=np.linspace(5,60,5501); pw=np.empty(len(gam))
for i in range(0,len(gam),250): pw[i:i+250]=np.abs(np.exp(-1j*np.outer(gam[i:i+250],u))@(g*w))*du
pk=[i for i in range(1,len(gam)-1) if pw[i]>pw[i-1] and pw[i]>pw[i+1] and pw[i]>0.02*pw.max()]
Z=[14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738,52.9703,56.4462,59.3470]
print("bulunan tepeler:",[round(gam[i],2) for i in pk])
print("bilinen sıfırlar:",Z)
