"""Kubik (ve diger) irrasyonellerde buyuk katsayilarin istatistigi, Gauss-Kuzmin ile karsilastirma."""
import math, numpy as np
from fractions import Fraction
from scipy import stats as st

LN2 = math.log(2)
def gk_tail(K): return math.log2(1 + 1 / K)          # P(a >= K)
def gk_pmf(k): return -math.log2(1 - 1 / (k + 1) ** 2)
def gauss_mu(lo, hi): return abs(math.log2((1 + hi) / (1 + lo)))
def cyl2(i, j):  # Gauss olcusu: a1=i, a2=j silindiri
    x1 = 1 / (i + 1 / j); x2 = 1 / (i + 1 / (j + 1)); return gauss_mu(min(x1, x2), max(x1, x2))

names = ['cbrt2', 'cbrt3', 'cbrt5', 'plastic', 'x3m3xm1', 'qrt2', 'pi', 'epi', 'ln2', 'pi2']
rows = []
pool = []
for nm in names:
    a = np.array([int(x) for x in np.load(f'data/{nm}.npy', allow_pickle=True).tolist()[1:100001]], dtype=np.int64)
    n = len(a)
    # 1) ki-kare: kategoriler 1..30 ve >=31
    cats = list(range(1, 31)); obs = [np.sum(a == k) for k in cats] + [np.sum(a >= 31)]
    exp = [n * gk_pmf(k) for k in cats] + [n * gk_tail(31)]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp)); p_chi = st.chi2.sf(chi2, len(obs) - 1)
    # 2) kuyruk: a>=10^j sayilari ve Poisson z
    tails = {}
    for j in (1, 2, 3, 4, 5):
        K = 10 ** j; o = int(np.sum(a >= K)); e = n * gk_tail(K); tails[K] = (o, e, (o - e) / math.sqrt(e))
    # 3) maksimum: P(max < M) ~ (1-gk_tail(M+1))^n
    M = int(a.max()); p_max = 1 - (1 - gk_tail(M + 1)) ** n   # P(max >= M+1 ... ) ust kuyruk
    Fmax = (1 - gk_tail(M + 1)) ** n                           # P(max <= M)
    # 4) ardisik ciftler (i,j<=4 ve geri kalan)
    pairs = {}
    for i in range(1, 5):
        for j in range(1, 5): pairs[(i, j)] = 0
    for x, y in zip(a[:-1], a[1:]):
        if x <= 4 and y <= 4: pairs[(x, y)] += 1
    o2 = np.array(list(pairs.values())); e2 = np.array([(n - 1) * cyl2(i, j) for (i, j) in pairs])
    chi2b = float(((o2 - e2) ** 2 / e2).sum()); p_pair = st.chi2.sf(chi2b, len(o2))  # yaklasik
    # 5) blok kararliligi: her 10^4'luk blokta a>=100 sayisi
    blk = [int(np.sum(a[i:i + 10000] >= 100)) for i in range(0, n, 10000)]
    rows.append((nm, n, chi2, p_chi, tails, M, Fmax, chi2b, p_pair, blk))
    if nm in names[:6]: pool.append(a)

print("GK beklenen a>=100 / 10^4 blok:", round(10000 * gk_tail(100), 1))
for r in rows:
    nm, n, chi2, p_chi, tails, M, Fmax, chi2b, p_pair, blk = r
    print(f"\n{nm}: n={n}  ki2(31 kat)={chi2:.1f} p={p_chi:.3f}  ciftler ki2={chi2b:.1f} p~{p_pair:.3f}")
    print("  kuyruk (gozlenen, beklenen, z):", {K: (o, round(e, 1), round(z, 2)) for K, (o, e, z) in tails.items()})
    print(f"  max={M}  P(max<=M | GK)={Fmax:.3f}   blok a>=100: {blk}")
# havuz: 6 cebirsel sayi (5 kubik + 2^(1/4)), kuyruk usteli
A = np.concatenate(pool); n = len(A)
print(f"\nHAVUZ (5 kubik + 2^(1/4)), n={n}")
for K in (2, 5, 10, 30, 100, 300, 1000, 3000, 10**4, 3 * 10**4, 10**5):
    o = int(np.sum(A >= K)); e = n * gk_tail(K)
    print(f"  a>={K:>6}: gozlenen {o:7d}  GK {e:10.1f}  oran {o/e:.3f}  z={(o-e)/math.sqrt(e):+.2f}")
# kuyruk usteli: log(sayim) ~ -alpha log K, GK'de alpha=1
Ks = np.array([10, 30, 100, 300, 1000, 3000, 10000]); cnt = np.array([np.sum(A >= K) for K in Ks])
alpha = -np.polyfit(np.log(Ks), np.log(cnt), 1)[0]
print(f"  kuyruk usteli (10..10^4 regresyon): {alpha:.3f}  (GK: ~1, K buyuk iken)")
