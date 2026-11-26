"""Harmoni uygarligi, Surum C: Euler'in muzik kurami, eşit olculer, Collatz komalari."""
import math, json, numpy as np, mpmath as mp
from fractions import Fraction
from sympy import factorint
mp.mp.dps = 80
res = {}
def gradus(n):  # Euler 1739: Γ(n) = 1 + Σ e_p (p-1)
    return 1 + sum(e*(p-1) for p, e in factorint(n).items())
def gradus_ratio(a, b):
    f = Fraction(a, b); return gradus(f.numerator*f.denominator)
iv = [('birlik', 1, 1), ('oktav', 2, 1), ('beşli', 3, 2), ('dörtlü', 4, 3), ('büyük altılı', 5, 3),
      ('büyük üçlü', 5, 4), ('küçük üçlü', 6, 5), ('küçük altılı', 8, 5), ('büyük ikili', 9, 8),
      ('küçük yedili', 16, 9), ('büyük yedili', 15, 8), ('küçük ikili', 16, 15), ('triton', 45, 32),
      ('Pisagor koması', 531441, 524288), ('sintonik koma', 81, 80)]
res['gradus_table'] = [(nm, f'{a}:{b}', gradus_ratio(a, b), round(1200*math.log2(a/b), 2)) for nm, a, b in iv]
# carpimsallik testi: Γ(mn)-1 = (Γ(m)-1)+(Γ(n)-1) tum m,n
bad = sum(gradus(m*n)-1 != gradus(m)-1+gradus(n)-1 for m in range(1, 300) for n in range(1, 300))
res['gradus_additive_errors_m,n<300'] = bad
# Tonnetz: 5-limit oranlar = (a,b,c) ussu: 2^a 3^b 5^c. Oktavi yok sayinca (b,c) kafesi.
res['tonnetz_examples'] = {'beşli 3/2': (1, 0), 'büyük üçlü 5/4': (0, 1), 'küçük üçlü 6/5': (1, -1),
                          'sintonik koma 81/80': (4, -1)}
alpha = mp.log(3, 2)
res['pythagorean_comma_cents'] = float(1200*(12*alpha-19))
res['mercator_comma_cents'] = float(1200*(53*alpha-84))
# surekli kesir ve yakinsaklar
a, x = [], alpha
for _ in range(14):
    a.append(int(mp.floor(x))); x = 1/(x-mp.floor(x))
res['cf_log2_3'] = a
p0, q0, p1, q1 = 1, 0, a[0], 1; conv = [(p1, q1)]
for ak in a[1:]:
    p0, q0, p1, q1 = p1, q1, ak*p1+p0, ak*q1+q0; conv.append((p1, q1))
res['convergents_K/L'] = [f'{p}/{q}' for p, q in conv]
# Esit olculer: beşli, büyük üçlü, küçük üçlü hatasi (cent); N-TET'te en yakin adim
def et_err(N):
    out = {}
    for nm, r in [('3/2', 1.5), ('5/4', 1.25), ('6/5', 1.2)]:
        c = 1200*math.log2(r); k = round(N*c/1200); out[nm] = round(k*1200/N - c, 3)
    return out
res['ET_errors_cents'] = {N: et_err(N) for N in [5, 7, 12, 19, 22, 31, 41, 53, 72, 306, 665]}
# hangi N icin beşli hatasi rekor kirar (1..700)?
rec, best = [], 1e9
for N in range(1, 701):
    e = abs(et_err(N)['3/2'])
    if e < best: best = e; rec.append((N, round(e, 4)))
res['ET_fifth_records_1_700'] = rec
# 5-limit kalite: max(|3/2|,|5/4|,|6/5|) rekorlari
rec, best = [], 1e9
for N in range(1, 701):
    e = max(abs(v) for v in et_err(N).values())
    if e < best: best = e; rec.append((N, round(e, 3)))
res['ET_5limit_records_1_700'] = rec

# ---- Collatz = koma problemi ----
# Dongu: L tek adim, K ikiye bolme. Carpim: 2^K/3^L = Π (1 + 1/(3 n_i)) (n_i tek elemanlar)
# Pozitif dongu => 2^K > 3^L ("tiz beşli"), negatif dongu => 2^K < 3^L ("pes beşli").
def collatz_cycle(n):
    seen, xs = {}, []
    while n not in seen:
        seen[n] = len(xs); xs.append(n); n = n//2 if n % 2 == 0 else 3*n+1
    cyc = xs[seen[n]:]; L = sum(v % 2 for v in cyc); K = len(cyc)-L
    return min(cyc, key=abs), K, L
cyc = {}
for n in list(range(1, 50)) + list(range(-300, 0)):
    m, K, L = collatz_cycle(n); cyc[m] = (K, L)
res['Z_cycles_(min, K, L, 3^L:2^K or 2^K:3^L, cents)'] = [
    (m, K, L, f'{max(2**K,3**L)}:{min(2**K,3**L)}', round(1200*abs(K-L*math.log2(3)), 2)) for m, (K, L) in sorted(cyc.items())]
# Kucuk L icin: pozitif dongunun en kucuk elemaninin ust siniri n_max(L)
tab = []
for L in range(1, 60):
    K = int(mp.ceil(L*alpha)); r = mp.mpf(2)**K/mp.mpf(3)**L
    nmax = 1/(3*(r**(mp.mpf(1)/L)-1))
    tab.append((L, K, round(float(1200*mp.log(r, 2)), 2), float(nmax)))
res['cycle_nmax_by_L_(L,K,comma_cents,nmax)'] = [t for t in tab if t[3] >= 0.5 or t[0] in (12, 41, 53)]
# Kesin alt sinir: tum elemanlar > N0 ise ln2*(K - L alpha) <= L ln(1+1/(3N0)) < L/(3N0)
#  => delta(L) = ceil(L alpha) - L alpha < L/C, C = 3 N0 ln 2.
# delta'nin rekorlari (ustten en iyi yaklasimlar) yari-yakinsaklar arasindadir.
cands = set()
pm, qm, pc, qc = 1, 0, a[0], 1
A2 = []
x = alpha
for _ in range(40):
    A2.append(int(mp.floor(x))); x = 1/(x-mp.floor(x))
pm, qm, pc, qc = 1, 0, A2[0], 1
for ak in A2[1:]:
    for i in range(0, ak+1): cands.add(qm+i*qc)
    pm, qm, pc, qc = pc, qc, ak*pc+pm, ak*qc+qm
cands = sorted(c for c in cands if c >= 1)
def delta(L): return mp.ceil(L*alpha) - L*alpha
recs, best = [], mp.mpf(2)
for q in cands:
    d = delta(q)
    if d < best: best = d; recs.append((q, d))
# dogrulama: L <= 2*10^5 icin kaba kuvvetle rekorlar ayni mi
bf, b = [], 2.0
la = float(alpha)
Ls = np.arange(1, 200001); dd = np.ceil(Ls*la) - Ls*la
for L, d in zip(Ls, dd):
    if d < b - 1e-12: b = d; bf.append(int(L))
res['record_check_bruteforce_2e5'] = [q for q, _ in recs if q <= 200000] == bf
out = {}
for name, N0 in [('2^68 (Barina 2021)', mp.mpf(2)**68), ('2^71 (Barina 2025)', mp.mpf(2)**71)]:
    C = 3*N0*mp.log(2); lb = None
    for j, (q, d) in enumerate(recs):
        qn = recs[j+1][0] if j+1 < len(recs) else 10**40
        cand = max(q, int(mp.floor(C*d))+1)
        if cand < qn: lb = cand; break
    first = next(q for q, d in recs if d < q/C)
    out[name] = dict(L_lower_bound=lb, first_record_L_satisfying=first,
                     its_K=int(mp.ceil(first*alpha)), comma_cents=float(1200*delta(first)))
res['collatz_min_odd_steps'] = out
res['records_upper_approx_(L, K, comma_cents)'] = [(q, int(mp.ceil(q*alpha)), mp.nstr(1200*d, 6)) for q, d in recs[:16]]
json.dump(res, open('/home/claude/civs/harmoni/sonuc_c.json', 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
