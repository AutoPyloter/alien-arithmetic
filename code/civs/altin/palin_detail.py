"""Zeckendorf palindromları: uzunluğa göre yerel (ortak elek) düzeltmeli model.
S_L = (küçük asallara (<200) aralarında asal palindrom oranı) / prod(1-1/l)."""
import math
from other_tests_lib import pals, val, mr
from sieve import small_primes
SP = [int(l) for l in small_primes(200)]
PR = math.prod(SP); D = math.prod(1 - 1 / l for l in SP)
print(" L    adet  çift oranı  asal  saf model  oran   S_L(ortak)  oran/S_L")
c3 = m3 = mS3 = 0
for L in range(16, 57):
    vs = [val(s) for s in pals(L)]
    S = sum(1 for v in vs if math.gcd(v, PR) == 1 or v in SP) / len(vs) / D
    c = sum(1 for v in vs if mr(v)); m = sum(1 / math.log(v) for v in vs)
    ev = sum(1 for v in vs if v % 2 == 0) / len(vs)
    r = f"{c/m/S:.3f}" if S > 0 else "  -  "
    print(f"{L:2d} {len(vs):7d}  {ev:.4f}  {c:6d} {m:9.1f}  {c/m:.3f}  {S:.3f}      {r}", flush=True)
    if L >= 30 and L % 3: c3 += c; m3 += m; mS3 += m * S
print(f"\nL=30..56, 3∤L toplam: gözlenen {c3}, saf model {m3:.1f} (oran {c3/m3:.4f}), ortak-elek düzeltmeli model {mS3:.1f} (oran {c3/mS3:.4f})")
