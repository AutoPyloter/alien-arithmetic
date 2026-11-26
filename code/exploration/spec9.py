import numpy as np, math
from mpmath import li
u,xs,ctw,cp=np.load('tw9.npy'); xs=xs.astype(float)
C2=0.6601618158
t=np.exp(np.linspace(math.log(2),math.log(1e9),800000))
def cumint(f):
    return np.concatenate([[0],np.cumsum((f[1:]+f[:-1])/2*np.diff(t))])
HL=2*C2*np.interp(xs,t,cumint(1/np.log(t)**2))
LI=np.interp(xs,t,cumint(1/np.log(t)))
gam=np.linspace(2,45,2151); du=u[1]-u[0]
def spec(e,uu):
    A=np.vstack([np.ones_like(uu),uu]).T; e=e-A@np.linalg.lstsq(A,e,rcond=None)[0]
    w=np.hanning(len(e)); out=np.empty(len(gam))
    for i in range(0,len(gam),300): out[i:i+300]=np.abs(np.exp(-1j*np.outer(gam[i:i+300],uu))@(e*w))*du
    return out
rng=np.random.default_rng(0)
def test(count,expect,name,nsur=60):
    e=(count-expect)/np.sqrt(xs); real=spec(e,u)
    inc=np.diff(np.concatenate([[0],expect])); sur=[]
    for _ in range(nsur):
        c=np.cumsum(rng.poisson(np.maximum(inc,0))); sur.append(spec((c-expect)/np.sqrt(xs),u))
    sur=np.array(sur); q99=np.quantile(sur,0.99,axis=0); med=np.median(sur,axis=0)
    ratio=real/q99
    pk=[i for i in range(1,len(gam)-1) if ratio[i]>ratio[i-1] and ratio[i]>ratio[i+1] and ratio[i]>1]
    print(name,": %99 eşiğini aşan tepe sayısı",len(pk))
    for i in sorted(pk,key=lambda i:-ratio[i])[:8]: print("   γ=%.2f  gerçek/eşik=%.2f  gerçek/medyan=%.1f"%(gam[i],ratio[i],real[i]/med[i]))
    return real,q99
rp,qp=test(cp,LI,"TEK HARFLER π(x)")
rt,qt=test(ctw,HL,"İKİZ HARFLER π2(x)")
np.save('spec9.npy',np.vstack([gam,rp,qp,rt,qt]))
# kararlılık: iki yarı
h=len(u)//2
for nm,cnt,ex in [("ikiz",ctw,HL)]:
    for a,b in [(0,h),(h,len(u))]:
        e=(cnt[a:b]-ex[a:b])/np.sqrt(xs[a:b]); s=spec(e,u[a:b])
        top=np.argsort(s)[-4:]; print(nm,"yarı",a,"tepe γ:",sorted(np.round(gam[top],1)))
