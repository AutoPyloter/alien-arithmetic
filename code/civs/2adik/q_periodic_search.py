"""Q (= Phi^{-1}) icin TEK rasyonel periyodik noktalari ara.
Q(x) her zaman paydasi (2^L-1)'i bolen bir rasyonel (x'in yorungesi donguye girerse).
Bu yuzden Q-periyodik rasyonel noktalar bu paydalarda aranir."""
from fractions import Fraction
from collatz2adic import Q_exact
import sys
LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
A = int(sys.argv[2]) if len(sys.argv) > 2 else 4
dens = set()
for L in range(1, LMAX+1):
    N = (1 << L) - 1
    dens |= {d for d in range(1, N+1, 2) if N % d == 0}
found = {}
tested = 0
for d in sorted(dens):
    for a in range(-A*d, A*d+1):
        if a % 2 == 0: continue          # yalniz tek noktalar
        x = Fraction(a, d)
        if x.denominator != d: continue
        tested += 1
        y = x
        for k in range(1, 9):
            y = Q_exact(y, 2*10**4)
            if y is None or y.denominator > 10**9: break
            if y == x:
                found.setdefault(k, set()).add(x); break
print(f'paydalar | 2^L-1 (L<={LMAX}), |x|<={A}, test edilen tek x: {tested}')
for k in sorted(found):
    print(f'  Q-periyodu {k}: {sorted(found[k])}')
