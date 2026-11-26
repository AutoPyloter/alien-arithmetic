"""Collatz sanisi kuyruk diliyle: Q(n) in (1/3)Z \\ Z  (n >= 1).
Negatif tamsayilar: Q(-n) paydasi 1 (…111, -1 dongusu), 7 (-5 dongusu) ya da 2047 (-17 dongusu)."""
from collections import Counter
from collatz2adic import Q_exact
N = 10**5
pos = Counter(Q_exact(n).denominator for n in range(1, N))
neg = Counter(Q_exact(-n).denominator for n in range(1, N))
print(f'1 <= n < {N}: Q(n) paydalari ->', dict(pos))
print(f'1 <= n < {N}: Q(-n) paydalari ->', dict(neg))
# 3Q(n) mod 3 ve 2-adik buyukluk: 3Q(n) = 3P - 2^s*(kuyruk), s = 1'e varis suresi civari
ex = [(n, Q_exact(n)) for n in (1, 2, 3, 5, 7, 27)]
for n, q in ex: print(f'  Q({n}) = {q}')
