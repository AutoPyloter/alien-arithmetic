"""Görev 2: (p mod l, q mod l) ortak dağılımı. q = floor((p+1)phi)-1 (altın kaydırma) ve kontrol q = floor(3p/2)."""
import sys, math, numpy as np
from sieve import primes_upto
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
P = primes_upto(X).astype(np.int64); P = P[P > 7]
def golden(P):
    m = P + 1; v = m * (1 + 5 ** .5) / 2; q = np.floor(v).astype(np.int64)
    bad = np.nonzero(np.abs(v - np.round(v)) < 1e-5)[0]
    for i in bad:
        mm = int(m[i]); q[i] = (mm + math.isqrt(5 * mm * mm)) // 2
    return q - 1
Q = {"altın kaydırma": golden(P), "3p/2 tabanı": (3 * P) // 2}
try:
    from scipy.stats import chi2
except Exception: chi2 = None
print(f"asallar 7 < p <= {X:.0e}: {len(P)} adet\n")
for name, q in Q.items():
    for l in (3, 5, 7):
        T = np.zeros((l, l), np.int64)
        np.add.at(T, (P % l, q % l), 1)
        T = T[1:]  # p mod l = 0 olamaz
        E = len(P) / ((l - 1) * l)
        x2 = ((T - E) ** 2 / E).sum(); dof = (l - 1) * l - 1
        pv = chi2.sf(x2, dof) if chi2 else float('nan')
        print(f"[{name}] l={l}: satır p mod l = 1..{l-1}, sütun q mod l = 0..{l-1}; değerler / beklenen")
        for a in range(l - 1): print("   ", " ".join(f"{T[a, j] / E:6.4f}" for j in range(l)))
        print(f"    ki-kare={x2:.1f} (sd={dof}), p-değeri={pv:.3g}\n")
    # yerel çarpan f_l = P(l ∤ q | p asal) / (1 - 1/l)
    fs = []; prod = 1.0
    for l in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        f = (q % l != 0).mean() / (1 - 1 / l); fs.append(f"{l}:{f:.4f}"); prod *= f
    print(f"[{name}] yerel çarpanlar f_l:", " ".join(fs), f"\n   çarpım (l<50) = {prod:.4f}\n")
