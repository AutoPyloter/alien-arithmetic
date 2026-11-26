"""Harmoni uygarligi, Surum B: n = frekansi ln n olan ton, n^{-it}.
Riemann acik formulu: psi0(x) = x - sum_rho x^rho/rho - ln(2pi) - 0.5 ln(1-x^-2)."""
import numpy as np, mpmath as mp, json, time, math
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sympy import primerange, factorint
K_MAX = 200
t0 = time.time()
try:
    g = np.load('/home/claude/civs/harmoni/zeros200.npy')
except FileNotFoundError:
    g = np.array([float(mp.zetazero(k).imag) for k in range(1, K_MAX+1)])
    np.save('/home/claude/civs/harmoni/zeros200.npy', g)
res = {'zeros_time_s': time.time()-t0, 'gamma1': g[0], 'gamma200': g[-1]}

def psi_K(x, K):
    x = np.asarray(x, float); rho = 0.5 + 1j*g[:K]
    w = np.exp(np.outer(np.log(x), rho))/rho          # her sifir bir dalga: x^rho/rho
    return x - 2*w.real.sum(1) - math.log(2*math.pi) - 0.5*np.log(1-x**-2.0)

def Lam(m):
    f = factorint(m); return math.log(next(iter(f))) if len(f) == 1 else 0.0
def psi_true(x):
    return np.array([sum(Lam(m) for m in range(2, int(np.floor(xx))+1)) for xx in x])

# 1) Grafik: basamakli psi ve K dalgadan yeniden kurulum
x = np.linspace(1.5, 50, 4000)
fig, ax = plt.subplots(2, 1, figsize=(10, 7.5))
ax[0].plot(x, psi_true(x), color='black', lw=1.6, label='ψ(x) (gerçek basamaklar)')
for K, c in [(10, '#c9a227'), (50, '#2a7ab0'), (200, '#c0392b')]:
    ax[0].plot(x, psi_K(x, K), color=c, lw=0.9, label=f'ilk {K} sıfırın dalgası')
ax[0].set_title('Harmoni B: asal basamakları zeta sıfırlarının dalgalarından kurmak (Riemann açık formülü)')
ax[0].set_xlabel('x'); ax[0].legend(frameon=False, fontsize=9); ax[0].grid(alpha=.2)
t = np.linspace(0, 60, 3000)
z = np.array([abs(mp.zeta(0.5+1j*tt)) for tt in t])
ax[1].plot(t, z, color='#2a7ab0', lw=1)
ax[1].plot(g[g < 60], 0*g[g < 60], 'o', color='#c0392b', ms=5, label='zeta sıfırları = sessiz frekanslar')
ax[1].set_title('Tüm tam sayıların akoru |ζ(1/2 + it)|: sustuğu yerler'); ax[1].set_xlabel('t (frekans)')
ax[1].legend(frameon=False); ax[1].grid(alpha=.2)
fig.tight_layout(); fig.savefig('/home/claude/civs/harmoni/acik_formul.png', dpi=110)

# 2) Sayisal hata: basamak ortalarinda (x = m + 1/2), 2 <= x <= 100
xm = np.arange(2, 100) + 0.5; tr = psi_true(xm)
err = {}
for K in [10, 25, 50, 100, 200]:
    e = psi_K(xm, K) - tr
    err[K] = dict(rms=float(np.sqrt((e**2).mean())), max=float(np.abs(e).max()))
res['error_midpoints_2_100'] = err
# 3) Kac sifir gerekir? m <= X icin sicrama J(m) = psi_K(m+.5)-psi_K(m-.5) ile
#    'asal kuvveti mi' karari (esik ln2/2). Tum m<=X dogru olan en kucuk K.
need = {}
for X in [10, 20, 30, 50, 75, 100, 150]:
    ms = np.arange(2, X+1); truth = np.array([Lam(int(m)) > 0 for m in ms])
    Kmin = None
    for K in range(1, K_MAX+1):
        J = psi_K(ms+0.5, K) - psi_K(ms-0.5, K)
        if np.all((J > math.log(2)/2) == truth): Kmin = K; break
    need[X] = (Kmin, float(g[Kmin-1]) if Kmin else None)
res['min_zeros_to_hear_prime_powers_upto_X_(K,gamma_K)'] = need
# 4) Euler carpimi: her asal ayri osilator. s=2'de P'ye kadar carpim
for s in [2.0, 1.5]:
    zs = float(mp.zeta(s)); out = []
    for P in [10, 100, 1000, 10000]:
        pr = np.array(list(primerange(2, P+1)), float)
        out.append((P, float(np.prod(1/(1-pr**-s)))/zs - 1))
    res[f'euler_product_rel_err_s={s}'] = out
# 5) RH 'ses yuksekligi' yasasi: Schoenfeld (RH altinda) |psi(x)-x| < sqrt(x) ln^2 x /(8pi), x>=73.2
M = 10**7
lam = np.zeros(M+1)
sieve = np.ones(M+1, bool); sieve[:2] = False
for p in range(2, int(M**.5)+1):
    if sieve[p]: sieve[p*p::p] = False
for p in np.nonzero(sieve)[0]:
    q = p
    while q <= M: lam[q] = math.log(p); q *= p
psi = np.cumsum(lam); xs = np.arange(M+1, dtype=float)
sel = xs >= 74
r1 = np.abs(psi[sel]-xs[sel]); r2 = np.abs(psi[sel]-(xs[sel]-1))   # basamagin iki ucu
r = np.maximum(r1, r2)/(np.sqrt(xs[sel])*np.log(xs[sel])**2/(8*np.pi))
res['schoenfeld_ratio_max_74_1e7'] = float(r.max())
res['max_|psi-x|/sqrt(x)_74_1e7'] = float((np.maximum(r1, r2)/np.sqrt(xs[sel])).max())
json.dump(res, open('/home/claude/civs/harmoni/sonuc_b.json', 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
