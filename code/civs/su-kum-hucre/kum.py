"""KUM uygarligi: Buffon ignesi, Monte Carlo, pi'nin basamak frekanslari."""
import math, numpy as np
from collections import Counter
from scipy.stats import chi2, kstest
rng = np.random.default_rng(12345)

def random_directions(n):
    """pi KULLANMADAN rastgele yon: birim diskten reddetme ornekleme."""
    out = np.empty((0, 2))
    while len(out) < n:
        p = rng.uniform(-1, 1, size=(2 * n, 2)); r2 = (p**2).sum(1)
        p = p[(r2 > 1e-12) & (r2 <= 1)]
        out = np.vstack([out, p / np.sqrt((p**2).sum(1))[:, None]])
    return out[:n]

def buffon(n, l=1.0, t=1.0, chunk=10**6):
    """Igne boyu l, cizgi araligi t (l<=t). Kesme olasiligi 2l/(pi t). pi_hat = 2 l n / (t * kesen)."""
    hits = 0; done = 0
    while done < n:
        m = min(chunk, n - done)
        y = rng.uniform(0, t / 2, m)                 # merkezin en yakin cizgiye uzakligi
        s = np.abs(random_directions(m)[:, 1])       # |sin(aci)|
        hits += int((y <= (l / 2) * s).sum()); done += m
    return 2 * l * n / (t * hits)

if __name__ == "__main__":
    print("== Buffon ignesi (l=t=1), yon pi'siz uretiliyor ==")
    for e in range(2, 8):
        n = 10**e; ph = buffon(n)
        print(f"N=10^{e}: pi_hat={ph:.6f}  hata={ph-math.pi:+.2e}  kuram SD={math.sqrt(math.pi**2*(math.pi-2)/2/n):.2e}")
    print("-- tekrarli deney: RMS hata * sqrt(N) (kuram sqrt(pi^2(pi-2)/2) = %.3f)" % math.sqrt(math.pi**2*(math.pi-2)/2))
    for e in (2, 3, 4, 5):
        n = 10**e; R = 400
        errs = np.array([buffon(n) - math.pi for _ in range(R)])
        print(f"N=10^{e}: RMS*sqrt(N) = {np.sqrt((errs**2).mean())*math.sqrt(n):.3f}")
    print("-- Lazzarini (1901) 3408 atis, l/t=5/6, 1808 kesis: pi_hat =", 2*(5/6)*3408/1808, "= 355/113?", abs(2*(5/6)*3408/1808 - 355/113) < 1e-12)

    print("\n== Monte Carlo: d-boyutlu birim top hacmi ==")
    n = 10**6
    for d in (2, 3, 5, 10, 15, 20):
        hits = 0
        for _ in range(4):
            x = rng.uniform(-1, 1, size=(n // 4, d)); hits += int(((x**2).sum(1) <= 1).sum())
        est = 2**d * hits / n; true = math.pi**(d/2) / math.gamma(d/2 + 1)
        relse = math.sqrt((1 - true/2**d) / (n * true/2**d)) if hits else float('inf')
        print(f"d={d:>2}: tahmin={est:.5g}  gercek={true:.5g}  isabet={hits}  goreli SD~{relse:.2e}")

    print("\n== pi'nin ilk 10^6 ondalik basamagi ==")
    d = open('pi_1e6.txt').read().strip(); N = len(d)
    a = np.frombuffer(d.encode(), dtype=np.uint8) - 48
    c = np.bincount(a, minlength=10); E = N / 10
    X = ((c - E)**2 / E).sum()
    print("rakam sayilari:", c.tolist()); print(f"ki-kare={X:.3f}, sd=9, p={chi2.sf(X, 9):.3f}")
    for k in (2, 3):
        m = N // k; blocks = a[:m*k].reshape(m, k) @ (10 ** np.arange(k-1, -1, -1))
        cb = np.bincount(blocks, minlength=10**k); E = m / 10**k
        X = ((cb - E)**2 / E).sum(); df = 10**k - 1
        print(f"{k}'li ortusmeyen bloklar: ki-kare={X:.1f}, sd={df}, p={chi2.sf(X, df):.3f}")
    # 10 parcada rakam ki-kare p-degerleri, uniform mu?
    ps = []
    for i in range(100):
        part = a[i*10**4:(i+1)*10**4]; cc = np.bincount(part, minlength=10); E = len(part)/10
        ps.append(chi2.sf(((cc-E)**2/E).sum(), 9))
    print("100 parcanin (10^4 basamak) rakam p-degerleri, KS uniform testi p =", round(kstest(ps, 'uniform').pvalue, 3))

    print("\n== Yeni deneme: tum k-basamakli dizilerin ilk kez ne zaman tamamlandigi ==")
    def complete_pos(arr, k):
        seen = np.zeros(10**k, bool); cnt = 0; v = 0; mod = 10**k
        for i, x in enumerate(arr):
            v = (v * 10 + int(x)) % mod
            if i >= k - 1 and not seen[v]:
                seen[v] = True; cnt += 1
                if cnt == mod: return i + 1
        return None
    for k in (2, 3, 4):
        pp = complete_pos(a, k)
        sims = [complete_pos(rng.integers(0, 10, size=400000), k) for _ in range(200 if k < 4 else 60)]
        sims = np.array(sims, float); rank = (sims < pp).mean()
        print(f"k={k}: pi'de tum 10^{k} dizi {pp}. basamakta tamam; rastgele: ort={sims.mean():.0f}, SD={sims.std():.0f}, pi'nin yuzdelik sirasi={rank:.2f}")
