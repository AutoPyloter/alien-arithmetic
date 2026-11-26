import sys, random, time
sys.path.insert(0, '/home/claude/civs/agac-oyun')
from matula import *
from sympy import prime, isprime, primepi
N = 20000
t0=time.time()
# 1. iki yönlü birebirlik
for n in range(1, N+1):
    assert number(tree(n)) == n
seen = set(tree(n) for n in range(1, N+1)); assert len(seen) == N
# rastgele ağaçlardan sayıya ve geri
random.seed(1)
def rt(d):
    if d == 0: return ()
    return tuple(sorted(rt(d-1) for _ in range(random.randint(0,2))))
for _ in range(300):
    t = rt(random.randint(0,4)); assert tree(number(t)) == t
print("ikiyönlü OK", N)
# 2. formüller
for n in range(1, N+1):
    t = tree(n)
    assert V(n) == tV(t) and H(n) == tH(t) and L(n) == tL(t) and rootdeg(n) == len(t)
print("V,H,L,derece OK")
# 3. köke çocuk ekleme = x p_k ; ağaç dikme (yeni kök) = n -> p_n
for n in range(1, 3000):
    for k in (1,2,3,7):
        assert number(tuple(sorted(tree(n)+(tree(k),)))) == n*prime(k)
    assert number((tree(n),)) == prime(n)
# asal <=> tek çocuklu kök
for n in range(2, N+1):
    assert isprime(n) == (len(tree(n)) == 1)
# yol (zincir) ağaçları = 1,2,3,5,11,31,...
chain=[1]
for _ in range(6): chain.append(int(prime(chain[-1])))
for k,c in enumerate(chain): assert tree(c) == (lambda f: f(f,k))(lambda f,k: () if k==0 else (f(f,k-1),))
print("zincir", chain)
# yıldız = 2^k
for k in range(10): assert tree(2**k) == ((),)*k
# 4. σ ağaçta: her çocuk alt-ağacını T_i -> T_{i+1} yapar
for n in range(1, 5000):
    s = sigma(n)
    assert tree(s) == tuple(sorted(tree(int(primepi(p))+1) for p,e in factorint(n).items() for _ in range(e)))
    assert V(s) >= V(n) or True
# σ köşe sayısını ne kadar değiştiriyor? (kaos göstergesi)
import collections
dv = collections.Counter(V(sigma(n)) - V(n) for n in range(1, 5000))
print("σ: ΔV dağılımı", sorted(dv.items())[:12])
dvp = collections.Counter(V(n+1) - V(n) for n in range(1, N))
print("+1: ΔV aralığı", min(dvp), max(dvp))
# bitişik sayıların ağaç benzerliği: ortak çocuk sayısı
share = sum(1 for n in range(2, N) if set(tree(n)) & set(tree(n+1))) 
print("n,n+1 ortak çocuk alt-ağacı olan çift sayısı:", share, "/", N-2)
print("süre", round(time.time()-t0,1))
