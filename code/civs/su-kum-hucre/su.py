"""SU uygarligi: kaplar, Bezout, en kisa dokme dizisi, Frobenius."""
import math, random, heapq
from collections import deque

def bfs_jugs(a, b):
    """(x,y) durumlari; 6 hamle. Her miktar c icin: kaplardan birinde c gorulen en az adim."""
    start = (0, 0); dist = {start: 0}; q = deque([start]); best = {}
    while q:
        x, y = q.popleft(); d = dist[(x, y)]
        for c in (x, y):
            if c not in best: best[c] = d
        t = min(x, b - y); u = min(y, a - x)
        for s in ((a, y), (x, b), (0, y), (x, 0), (x - t, y + t), (x + u, y - u)):
            if s not in dist:
                dist[s] = d + 1; q.append(s)
    return best, len(dist)

def formula_steps(a, b, c):
    """Iki saf strateji (A->B ve B->A: bos olani doldur, dolu olani bosalt, aradakini dok) simule edilir; minimum alinir."""
    def sim(A, B, c):  # A'dan B'ye dok stratejisi
        x = y = 0; n = 0
        for _ in range(4 * (A + B) + 10):
            if x == c or y == c: return n
            if x == 0: x = A
            elif y == B: y = 0
            else:
                t = min(x, B - y); x -= t; y += t
            n += 1
        return None
    r = [s for s in (sim(a, b, c), sim(b, a, c)) if s is not None]
    return min(r) if r else None

def closed_steps(a, b, c):
    if c == a: return 1
    x = next(x for x in range(1, b + 1) if (x * a - c) % b == 0); y = (x * a - c) // b
    s1 = 2 * (x + y) - (2 if c < a else 0)
    x2 = next(x for x in range(1, a + 1) if (x * b - c) % a == 0); y2 = (x2 * b - c) // a
    return min(s1, 2 * (x2 + y2) - 2)

def frob2(a, b): return a * b - a - b

def frob_dijkstra(gens):
    """En kucuk ureteç a modunda en kisa yollar (Nijenhuis/Bocker-Liptak fikri). F = max dist - a."""
    a = min(gens); others = [g for g in gens if g != a]
    INF = float('inf'); dist = [INF] * a; dist[0] = 0; pq = [(0, 0)]
    while pq:
        d, r = heapq.heappop(pq)
        if d > dist[r]: continue
        for g in others:
            s = (r + g) % a
            if d + g < dist[s]:
                dist[s] = d + g; heapq.heappush(pq, (d + g, s))
    if INF in dist: return None
    return max(dist) - a

def frob_brute(gens, lim=None):
    lim = lim or (max(gens) ** 2 + 10)
    ok = [False] * (lim + 1); ok[0] = True
    for n in range(1, lim + 1):
        ok[n] = any(n >= g and ok[n - g] for g in gens)
    bad = [n for n in range(lim + 1) if not ok[n]]
    return bad[-1] if bad else -1

if __name__ == "__main__":
    random.seed(1)
    # 1) Bezout: c elde edilir <=> c <= max(a,b) ve gcd | c
    err = 0; tot = 0
    for a in range(1, 31):
        for b in range(a, 31):
            best, _ = bfs_jugs(a, b); g = math.gcd(a, b)
            for c in range(0, b + 1):
                tot += 1
                if (c in best) != (c % g == 0): err += 1
    print("Bezout testi (a<=b<=30):", tot, "durum,", err, "hata")
    # 2) en kisa dizi: BFS vs iki-strateji simulasyonu
    err = 0; tot = 0; maxsteps = 0; arg = None
    for a in range(1, 31):
        for b in range(a, 31):
            best, _ = bfs_jugs(a, b)
            for c, d in best.items():
                if c == 0: continue
                tot += 1
                f = formula_steps(a, b, c)
                if f != d: err += 1
                if d > maxsteps: maxsteps, arg = d, (a, b, c)
    print("En kisa dizi = iki saf stratejinin minimumu:", tot, "durum,", err, "hata; en uzun:", maxsteps, arg)
    # 2b) kapali form (a<b aralarinda asal, 0<c<b, c!=a):
    #   a->b: x a - y b = c, x>=1 en kucuk;  adim 2(x+y) - 2*[c<a]
    #   b->a: x'b - y'a = c, x'>=1 en kucuk; adim 2(x'+y') - 2
    err = 0; tot = 0
    for a in range(1, 31):
        for b in range(a + 1, 31):
            g = math.gcd(a, b)
            best, _ = bfs_jugs(a, b)
            for c, d in best.items():
                if c == 0 or c == b: continue
                tot += 1
                if closed_steps(a // g, b // g, c // g) != d: err += 1
    print("Kapali form (a<b<=30, gcd'ye bolerek):", tot, "durum,", err, "hata")
    # 2c) en zor miktar: M(a,b) = max_c adim
    rows = []
    for a in range(1, 31):
        for b in range(a + 1, 31):
            if math.gcd(a, b) != 1: continue
            best, _ = bfs_jugs(a, b)
            M = max(best.values())
            rows.append((a, b, M))
    viol = [(a, b, M) for a, b, M in rows if M > 2 * (b - 2) and b > 2]
    eq = [(a, b) for a, b, M in rows if M == 2 * (b - 2)]
    print("M(a,b) <= 2(b-2) ihlali (b>2):", len(viol), "; esitlik:", len(eq), "/", len(rows), eq[:25])
    print("b=a+1 icin M:", [(a, b, M) for a, b, M in rows if b == a + 1][:8])
    # 3) Iki kap Frobenius
    err = 0
    for a in range(2, 41):
        for b in range(a + 1, 41):
            if math.gcd(a, b) == 1 and frob_brute([a, b]) != frob2(a, b): err += 1
    print("Sylvester ab-a-b (2<=a<b<=40):", err, "hata")
    # 4) Uc kap: Dijkstra vs kaba kuvvet
    err = 0; n = 0
    for a in range(2, 26):
        for b in range(a + 1, 26):
            for c in range(b + 1, 26):
                if math.gcd(math.gcd(a, b), c) != 1: continue
                n += 1
                if frob_dijkstra([a, b, c]) != frob_brute([a, b, c]): err += 1
    print("Dijkstra vs kaba kuvvet (uc kap <=25):", n, "uclu,", err, "hata")
    # 5) Olcekleme: rastgele uclular, (F+a+b+c)/sqrt(abc)
    for N in (10**3, 10**4, 10**5):
        vals = []; davison = 0
        while len(vals) < 2000:
            a, b, c = sorted(random.sample(range(2, N), 3))
            if math.gcd(math.gcd(a, b), c) != 1: continue
            F = frob_dijkstra([a, b, c]); s = math.sqrt(a * b * c)
            vals.append((F + a + b + c) / s)
            if F < math.sqrt(3 * a * b * c) - a - b - c: davison += 1
        m = sum(vals) / len(vals)
        print(f"N={N}: ort (F+a+b+c)/sqrt(abc) = {m:.4f} (8/pi={8/math.pi:.4f}), min={min(vals):.4f} (sqrt3={math.sqrt(3):.4f}), Davison ihlali={davison}")

def M_closed(a, b):
    return max(closed_steps(a, b, c) for c in range(1, b))

if __name__ == "__main__":
    # 2d) kapali formla daha genis test: b <= 150
    viol = 0; eqs = []; n = 0
    for a in range(1, 151):
        for b in range(a + 1, 151):
            if math.gcd(a, b) != 1 or b < 5: continue
            n += 1; M = M_closed(a, b)
            if M > 2 * (b - 2): viol += 1
            if M == 2 * (b - 2): eqs.append((a, b))
    other = [(a, b) for a, b in eqs if not (b - a == 1 or (b - a == 2 and a % 2 == 1))]
    print(f"b<=150 (5<=b), {n} cift: M>2(b-2) ihlali={viol}; esitlik={len(eqs)}; b-a=1 veya (b-a=2, a tek) disi esitlik: {other}")
    # BFS ile kapali formun buyuk b'de capraz kontrolu (rastgele 200 cift, b<=150)
    random.seed(7); bad = 0
    for _ in range(200):
        b = random.randint(5, 150); a = random.randint(1, b - 1)
        if math.gcd(a, b) != 1: continue
        best, _ = bfs_jugs(a, b)
        if any(closed_steps(a, b, c) != best[c] for c in range(1, b)): bad += 1
    print("BFS capraz kontrol (rastgele, b<=150):", bad, "hata")
