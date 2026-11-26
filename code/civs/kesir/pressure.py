"""Sezgisel hesap: Toplami s olan kompozisyonlarin surekli kesir paydalari K(c).
p(theta) = lim (1/s) log sum_{c |- s} K(c)^theta.  h(y) = inf_theta [p(theta) - theta*y]
(paydasi ~e^{ys} olan kompozisyon sayisi ~ e^{s h(y)}). Tipik q~e^L icin kapsanma:
h(y) >= y  ->  y* : h(y*) = y*,  S(q) ~ L / y*,  kappa = log(phi)/y*."""
import numpy as np, math
from numpy.polynomial import chebyshev as Ch
phi = (1 + 5 ** .5) / 2
nodes = 0.5 + 0.5 * np.cos(np.pi * (np.arange(48) + 0.5) / 48)   # [0,1] icinde
def p_of(theta, S=400, A=250):
    logc = [0.0]; gs = [np.ones_like(nodes)]   # G_0 = 1
    fits = [Ch.chebfit(2 * nodes - 1, gs[0], 30)]
    for s in range(1, S + 1):
        terms = []
        for a in range(1, min(s, A) + 1):
            x = nodes; y = 1 / (a + x)
            g = Ch.chebval(2 * y - 1, fits[s - a])
            terms.append((logc[s - a], theta * np.log(a + x) + np.log(np.maximum(g, 1e-300))))
        m = max(t[0] + t[1].max() for t in terms)
        tot = sum(np.exp(t[0] + t[1] - m) for t in terms)
        logc.append(m); gs.append(tot); fits.append(Ch.chebfit(2 * nodes - 1, tot, 30))
    lg = lambda s: logc[s] + math.log(Ch.chebval(-1.0, fits[s]))   # x=0 -> 2x-1=-1
    return (lg(S) - lg(S - 100)) / 100
import sys
th = np.linspace(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else np.linspace(0, 12, 49)
P = np.array([p_of(t) for t in th])
print("p(0)=%.5f (log2=%.5f)  p(1)=%.5f  p(12)/12=%.5f (log phi=%.5f)" % (P[0], math.log(2), P[min(4,len(P)-1)], P[-1] / th[-1], math.log(phi)))
# p(1) teorik: sum_c K(c) ~ ? (lineer): kontrol icin dogrudan
dP = np.gradient(P, th)
# p(theta) = (1+theta) p'(theta) kok
f = P - (1 + th) * dP
i = np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]
for j in i:
    t0 = th[j] - f[j] * (th[j + 1] - th[j]) / (f[j + 1] - f[j])
    y = np.interp(t0, th, dP)
    print(f"theta*={t0:.3f}  y*={y:.5f}  kappa=log(phi)/y*={math.log(phi)/y:.4f}  (E/k ~ kappa-1 = {math.log(phi)/y - 1:.4f})")
for t_, p_, d_, f_ in zip(th[::4], P[::4], dP[::4], f[::4]):
    print(f"  theta={t_:5.2f} p={p_:.5f} p'={d_:.5f} y=p' h=p-theta*p'={p_-t_*d_:.5f}  f={f_:+.5f}")
