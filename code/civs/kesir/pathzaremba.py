"""Yol uygarliginin Zaremba'si: S(q) = min_a (a/q'nun kismi bolum toplami) = 1 + min Stern-Brocot derinligi.
Alt sinir: F_{s+1} >= q olan en kucuk s. Fazlalik E(q) = S(q) - s_min(q)."""
import sys, math, numpy as np
fn = sys.argv[1] if len(sys.argv) > 1 else 'data/z60000.txt'
d = np.loadtxt(fn, skiprows=1, dtype=np.int64)
d = d[d[:, 0] >= 2]
if len(d) and d[-1, 0] != d[-2, 0] + 1: d = d[:-1]
q, Z, S = d[:, 0], d[:, 1], d[:, 2]
F = [0, 1]
while F[-1] < 10**12: F.append(F[-1] + F[-2])
smin = np.array([next(s for s in range(1, 200) if F[s + 1] >= x) for x in q])
E = S - smin
N = q[-1]
print(f"N={N}")
print("Zaremba: Z(q)=5 olan q:", q[Z >= 5].tolist(), "  Z=4 sayisi:", int((Z == 4).sum()), " Z=3:", int((Z == 3).sum()))
print("S(2..30):", S[:29].tolist())
print("E dagilimi:", {int(k): int((E == k).sum()) for k in np.unique(E)})
rec = []; m = -1
for x, e in zip(q, E):
    if e > m: m = e; rec.append((int(x), int(e)))
print("E rekorlari (q, E):", rec)
# S(q)/log_phi(q)
phi = (1 + 5 ** .5) / 2
r = S / (np.log(q) / math.log(phi))
for lo, hi in [(1000, 3000), (3000, 10000), (10000, 30000), (30000, N + 1)]:
    m_ = (q >= lo) & (q < hi)
    if m_.any(): print(f"  q in [{lo},{hi}): ortalama E={E[m_].mean():.3f} max E={E[m_].max()} ortalama S/log_phi q={r[m_].mean():.4f}")
# Zaremba ile iliski: Z(q) buyuk olan q'larda E buyuk mu?
for z in (2, 3, 4, 5):
    m_ = (Z == z) & (q > 100)
    if m_.any(): print(f"  Z={z}: n={m_.sum()}, ortalama E={E[m_].mean():.3f}")
# surekli normalizasyon: C(q) = S(q) - log_phi(sqrt5 * q)  (Fibonacci q=F_{s+1} icin ~ 0)
C = S - np.log(math.sqrt(5) * q) / math.log(phi)
for lo, hi in [(10, 100), (100, 1000), (1000, 10000), (10000, 30000), (30000, N + 1)]:
    m_ = (q >= lo) & (q < hi)
    i = np.argmax(np.where(m_, C, -99))
    print(f"  C(q) [{lo},{hi}): max={C[i]:.3f} (q={q[i]}), ortalama={C[m_].mean():.3f}")
