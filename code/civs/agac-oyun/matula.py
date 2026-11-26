"""AĞAÇ uygarlığı: Matula–Göbel numaralandırması.
Sayı n = prod p_i^e  <->  köklü ağaç; kökün çocukları i'lerin ağaçları (e kez).
Ağaç temsili: çocukların sıralı demeti (tuple) — kanonik, sıralı.
"""
from functools import lru_cache
from sympy import factorint, prime, primepi

@lru_cache(maxsize=None)
def tree(n):
    """n -> kanonik köklü ağaç (çocuk ağaçlarının sıralı tuple'ı)."""
    if n == 1:
        return ()
    kids = []
    for p, e in factorint(n).items():
        kids += [tree(int(primepi(p)))] * e
    return tuple(sorted(kids))

@lru_cache(maxsize=None)
def number(t):
    """köklü ağaç -> Matula numarası."""
    r = 1
    for c in t:
        r *= _prime(number(c))
    return r

@lru_cache(maxsize=None)
def _prime(k):
    return int(prime(k))

def show(t):
    return "(" + "".join(show(c) for c in t) + ")"

# --- sayı-kuramsal formüller (ağaçta kolay işlemler) ---
@lru_cache(maxsize=None)
def V(n):   # köşe sayısı: V(1)=1, V(p_i)=1+V(i), V(ab)=V(a)+V(b)-1
    if n == 1: return 1
    return 1 + sum(e * V(int(primepi(p))) for p, e in factorint(n).items())

@lru_cache(maxsize=None)
def H(n):   # yükseklik: H(1)=0, H(p_i)=1+H(i), H(ab)=max
    if n == 1: return 0
    return 1 + max(H(int(primepi(p))) for p in factorint(n))

@lru_cache(maxsize=None)
def L(n):   # yaprak sayısı (kök hariç; L(1)=0, L(2)=1), L(ab)=L(a)+L(b)
    if n == 1: return 0
    return sum(e * (1 if p == 2 else L(int(primepi(p)))) for p, e in factorint(n).items())

def rootdeg(n):  # kök derecesi = Omega(n)
    return sum(factorint(n).values())

@lru_cache(maxsize=None)
def G(n):   # Green Hackenbush değeri: G(1)=0, G(p_i)=G(i)+1, G(ab)=G(a) XOR G(b)
    if n == 1: return 0
    r = 0
    for p, e in factorint(n).items():
        if e % 2: r ^= G(int(primepi(p))) + 1
    return r

# --- doğrudan ağaç üzerinde (bağımsız) hesaplar ---
def tV(t): return 1 + sum(tV(c) for c in t)
def tH(t): return 0 if not t else 1 + max(tH(c) for c in t)
def tL(t): return 0 if not t else sum(1 if not c else tL(c) for c in t)

def sigma(n):  # harf kaydırma: p_i -> p_{i+1}
    r = 1
    for p, e in factorint(n).items():
        r *= prime(int(primepi(p)) + 1) ** e
    return r

def unrooted_canon(t):
    """köklü ağacı köksüz ağaca çevir; tüm köklemeler içinde en küçük Matula numarasını döndür."""
    # komşuluk listesi kur
    adj = []
    def build(t, parent):
        v = len(adj); adj.append([])
        if parent is not None:
            adj[v].append(parent); adj[parent].append(v)
        for c in t: build(c, v)
        return v
    build(t, None)
    def rooted_at(r):
        def rec(v, par):
            return tuple(sorted(rec(w, v) for w in adj[v] if w != par))
        return rec(r, None)
    # sadece merkez(ler)de köklemek yetmez (en küçük numara başka köşede olabilir), hepsini dene
    return min(number(rooted_at(r)) for r in range(len(adj)))
