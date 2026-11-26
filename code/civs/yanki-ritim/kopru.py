"""Köprü: ritim = yankının zamanda oynatılması."""
import math
from sympy import primerange
base = [2, 3, 5, 7]
print("t  : yankı (t mod 2,3,5,7) | davullar (x = o davul bu vuruşta çalıyor)")
for t in range(0, 16):
    y = tuple(t % p for p in base)
    print(f"{t:2d} : {y} | " + " ".join("x" if r == 0 else "." for r in y) + ("   <- sessiz vuruş (ebob(t,210)=1)" if all(y) else ""))
# Jacobsthal: davullar 2..p birlikte çalarken en uzun 'hiç sessiz vuruş olmayan' aralık + 1
print("Jacobsthal j(p#): en uzun sessizlik-siz koşu + 1 (davullar 2..p)")
for p in [3, 5, 7, 11, 13, 17, 19]:
    P = math.prod(primerange(2, p + 1)); silent = [t for t in range(1, 2 * P + 1) if math.gcd(t, P) == 1]
    print(f"  p={p:2d}: j = {max(b - a for a, b in zip(silent, silent[1:]))}")
