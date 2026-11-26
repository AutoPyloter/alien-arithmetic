"""Yeni gozlem testi: asama-2 noktalarinin (60 derece baslangici) iki-nokta yonleri,
20 ve 40 dereceye (mod 60) ne kadar yaklasiyor? Tekduze (rastgele yon) modeliyle karsilastirma.
Girdi: out/pts60_s2.txt (stages.py uretir). Cift duyarlik yeterli (eps >= 1e-7 derece)."""
import numpy as np

P = np.loadtxt("out/pts60_s2.txt")[:, :2]
n = len(P)
i, j = np.triu_indices(n, 1)
ang = np.degrees(np.arctan2(P[j, 1] - P[i, 1], P[j, 0] - P[i, 0])) % 60.0
# ayni yonu (paralel dogrular) bir kez say
dirs = np.unique(np.round(ang, 9))
D = len(dirs)
print(f"{n} nokta, {len(ang)} cift, {D} farkli yon (mod 60, 1e-9 derece cozunurluk)")
err = np.minimum(np.abs(dirs - 20), np.abs(dirs - 40))
print(f"en yakin yon hatasi: {err.min():.3e} derece")
for eps in (1.0, 0.1, 0.01, 0.001, 1e-4):
    obs = int((err < eps).sum())
    exp = D * 4 * eps / 60
    print(f"  eps={eps:<7}: gozlenen {obs:>7}, tekduze model {exp:>10.1f}, oran {obs/exp if exp else float('nan'):.3f}")
# karsilastirma: rastgele hedef acilar (ornegin 17.3, 23.9...) icin ayni istatistik
rng = np.random.default_rng(1)
for tgt in rng.uniform(0, 60, 5):
    e2 = np.minimum(np.abs(dirs - tgt), 60 - np.abs(dirs - tgt))
    print(f"  hedef {tgt:7.3f}: en yakin {e2.min():.3e}, eps=0.01 icinde {(e2 < 0.01).sum()} (model {D*2*0.01/60:.1f})")
# 0 ve 30 derece (insa edilebilir hedefler) icin
for tgt in (0.0, 30.0, 15.0):
    e2 = np.minimum(np.abs(dirs - tgt), 60 - np.abs(dirs - tgt))
    print(f"  insa edilebilir hedef {tgt}: tam isabet (1e-9) {(e2 < 1e-9).sum()}, eps=0.01 icinde {(e2 < 0.01).sum()}")

print("\n-- hedef basina yogunluk orani (gozlenen / tekduze model), pencere +-eps --")
targets = [("insa", t) for t in (0.0, 3.0, 6.0, 12.0, 15.0, 30.0, 45.0, 7.5)] + \
          [("insa-degil", t) for t in (20.0, 40.0, 10.0, 1.0, 50.0, 25.0, 35.0)] + \
          [("rastgele", float(t)) for t in rng.uniform(0, 60, 6)]
for eps in (0.1, 0.01, 0.001):
    row = []
    for kind, tgt in targets:
        e2 = np.abs((dirs - tgt + 30) % 60 - 30)
        row.append((kind, tgt, (e2 < eps).sum() / (D * 2 * eps / 60)))
    for kind in ("insa", "insa-degil", "rastgele"):
        vals = [r for k, t, r in row if k == kind]
        print(f"  eps={eps:<6} {kind:<11}: " + " ".join(f"{t:g}:{r:.2f}" for k, t, r in row if k == kind)
              + f"  | ort {np.mean(vals):.2f}")

print("\n-- {0,1} asama 2 (203 nokta): iki nokta uzakligi ile kup kok 2'ye en iyi yaklasim --")
Q = np.loadtxt("out/pts01_s2.txt")[:, :2]
a, b = np.triu_indices(len(Q), 1)
dist = np.hypot(Q[a, 0] - Q[b, 0], Q[a, 1] - Q[b, 1])
c = 2 ** (1 / 3)
k = np.argmin(np.abs(dist - c))
print(f"  en iyi uzaklik {dist[k]:.10f}, hata {abs(dist[k]-c):.3e}  ({len(np.unique(np.round(dist, 9)))} farkli uzaklik)")
