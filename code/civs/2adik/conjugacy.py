"""Bernstein–Lagarias eslenik haritasi: Phi = Q^{-1}. Q mod 2^n permutasyonunun
mertebesi ve dongu yapisi; Q'nun kucuk yukseklikli rasyonel periyodik noktalari."""
from fractions import Fraction
from math import lcm
from collections import Counter
from collatz2adic import Qk, Q_exact

print('== sigma_n = Q mod 2^n : mertebe ve dongu uzunluklari')
for n in range(1, 19):
    N = 1 << n
    perm = [Qk(x, n) for x in range(N)]
    seen = [False]*N
    lens = Counter()
    for s in range(N):
        if not seen[s]:
            L, x = 0, s
            while not seen[x]: seen[x] = True; x = perm[x]; L += 1
            lens[L] += 1
    order = 1
    for L in lens: order = lcm(order, L)
    longest = max(lens)
    print(f'  n={n:2d} mertebe={order:6d}  2^(n-4)={2**(n-4) if n>=4 else "-":>6}  '
          f'en uzun dongu={longest} (adet {lens[longest]})  sabit nokta={lens[1]}')

print()
print('== Q\'nun rasyonel sabit ve 2-periyodik noktalari, x=a/d, |a|<=300, d<=63 tek')
fixed, two = set(), set()
fail = 0
for d in range(1, 64, 2):
    for a in range(-300, 301):
        x = Fraction(a, d)
        if x.denominator != d: continue
        y = Q_exact(x, 10**5)
        if y is None: fail += 1; continue
        if y == x: fixed.add(x); continue
        if y.denominator < 10**6:
            z = Q_exact(y, 10**5)
            if z == x: two.add(frozenset((x, y)))
print('  sabit noktalar:', sorted(fixed))
print('  2-dongu sayisi:', len(two))
for c in sorted(two, key=lambda s: min(abs(t) for t in s))[:40]:
    print('   ', sorted(c, key=abs))
print('  Q hesaplanamayan (limit) baslangic sayisi:', fail)
