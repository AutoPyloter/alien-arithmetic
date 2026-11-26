"""Yeni soru: "cift periyodik" T-donguleri.
Bir p-dongusundeki x'in parite dizisi p-periyotludur (Q(x) paydasi 2^p-1'i boler).
x'in KENDI ikili yazisi da p-periyotlu olabilir mi? Bu, indirgenmis paydanin
g = gcd(2^p-1, 3^m-1)'i bolmesi demek. Tamsayi donguler (payda 1) bunun en basit hali."""
from math import gcd
from fractions import Fraction
import sys
sys.setrecursionlimit(10000)
sys.set_int_max_str_digits(10**6)
from collatz2adic import Q_exact, ordmod, T

def necklace_words(p):
    """Ilkel kolyeler (Duval / FKM algoritmasi), kanonik = en kucuk donme (liste, v_0 ilk)."""
    a = [0]*(p+1)
    def gen(t, q):
        if t > p:
            if p % q == 0 and q == p: yield tuple(a[1:])
        else:
            a[t] = a[t-q]
            yield from gen(t+1, q)
            for j in range(a[t-q]+1, 2):
                a[t] = j
                yield from gen(t+1, t)
    yield from gen(1, 1)

def c_of(v):
    # T^p(x) = (3^m x + c)/2^p ; tek adimda (a x + b) -> (3a x + 3b + 2^i)/... ile tamsayi tut
    # x_i = (3^{k_i} x + c_i) / 2^i ; tek: x_{i+1} = (3 x_i + 1)/2 = (3^{k+1} x + 3c_i + 2^i)/2^{i+1}
    c = 0
    for i, b in enumerate(v):
        if b: c = 3*c + (1 << i)
    return c

def bits_word(x, L):
    """2-adik x'in ilk L hanesi (v_0 ilk)."""
    n = x.numerator * pow(x.denominator, -1, 1 << L) % (1 << L)
    return tuple((n >> i) & 1 for i in range(L))

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
found = []
for p in range(1, PMAX+1):
    for v in necklace_words(p):
        m = sum(v)
        D = (1 << p) - 3**m
        g = gcd((1 << p) - 1, 3**m - 1) if m else 1
        c = c_of(v)
        if c % (abs(D)//gcd(abs(D), g)) == 0:
            found.append((p, m, v, Fraction(c, D)))
print(f'p <= {PMAX}: cift periyodik donguler')
for p, m, v, x in found:
    d = x.denominator
    # dongudeki her noktanin ikili kelimesi ile parite kelimesinin donmelerini karsilastir
    orb = [x]
    for _ in range(p-1):
        y = orb[-1]
        orb.append(y/2 if y.numerator % 2 == 0 else (3*y+1)/2)
    rots = {v[r:]+v[:r] for r in range(p)}
    selfsim = [o for o in orb if bits_word(o, 3*p)[:p] in rots and ordmod(d) and p % ordmod(d) == 0]
    # Q(x) ve Q(Q(x))
    q1 = Q_exact(x)
    q2 = Q_exact(q1) if q1 is not None else None
    print(f' p={p:2d} m={m:2d} kelime={"".join(map(str,v))} payda={d} '
          f'x={x}  Q(x)={q1}  Q(Q(x)) paydasi {len(str(q2.denominator)) if q2 is not None else None} haneli')
