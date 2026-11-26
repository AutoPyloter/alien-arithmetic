"""Yol-Zaremba (E(q) <= c) => Kesir-Zaremba (Z(q) <= A*(c)).
a/q = [0;a1..an], toplam s, q = K(a1..an). E(q)<=c ise optimum a icin s <= s_min(q)+c ve
q > F_{s_min} >= F_{s-c}. Bir kismi bolum >= A ise q <= M(s,A) (A disindakiler 1 iken maksimum).
M(s,A) <= F_{s-c} olan A'lar imkansiz; A*(c) = mumkun en buyuk A."""
from itertools import product
F = [0, 1]
for _ in range(200): F.append(F[-1] + F[-2])
def K(seq):
    p0, p1 = 1, 0
    # K() = 1, K(a)=a, K(a,b)=ab+1
    k0, k1 = 0, 1
    for a in seq: k0, k1 = k1, a * k1 + k0
    return k1
def comps(s):
    if s == 0: yield (); return
    for a in range(1, s + 1):
        for r in comps(s - a): yield (a,) + r
# 1) brute-force: M(s,A) = max K over compositions of s with a part >= A, vs formula with ones
def M_formula(s, A):
    best = 0
    for B in range(A, s + 1):
        for i in range(0, s - B + 1):
            j = s - B - i
            best = max(best, B * F[i + 1] * F[j + 1] + F[i] * F[j + 1] + F[i + 1] * F[j])
    return best
ok = True
for s in range(1, 19):
    allc = list(comps(s))
    for A in range(1, s + 1):
        bf = max(K(c) for c in allc if max(c) >= A)
        if bf != M_formula(s, A): ok = False; print("FARK", s, A, bf, M_formula(s, A))
print("M(s,A) formulu (birler + tek buyuk parca) s<=18 brute-force ile ayni:", ok)
# 2) A*(c)
for c in range(0, 7):
    Astar = 0
    for s in range(1, 120):
        for A in range(1, s + 1):
            if M_formula(s, A) > F[max(s - c, 0)]: Astar = max(Astar, A)
    print(f"c={c}: E(q)<=c  =>  Z(q) <= {Astar}")
