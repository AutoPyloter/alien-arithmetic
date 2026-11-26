"""Arnold/Ustinov olcekleme testi: (F+a+b+c)/sqrt(abc) ortalamasi ~ 8/pi."""
import math, random, statistics
from su import frob_dijkstra
random.seed(2026)
for N, K in ((10**3, 20000), (10**4, 20000), (10**5, 4000)):
    v = []
    while len(v) < K:
        a, b, c = sorted(random.sample(range(2, N + 1), 3))
        if math.gcd(math.gcd(a, b), c) != 1: continue
        v.append((frob_dijkstra([a, b, c]) + a + b + c) / math.sqrt(a * b * c))
    m = statistics.mean(v); se = statistics.stdev(v) / math.sqrt(K)
    med = statistics.median(v)
    print(f"N={N:>6} K={K}: ortalama={m:.4f} +- {se:.4f}  medyan={med:.4f}  min={min(v):.4f}  max={max(v):.1f}  8/pi={8/math.pi:.4f}")
