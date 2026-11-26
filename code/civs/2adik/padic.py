"""Sonsuz-sol (2-adik) uygarlik: kesik 2-adik sayilar.
Bir 2-adik tamsayi, K hanelik pencereyle (mod 2^K) temsil edilir.
Payda tek oldugu surece rasyoneller de 2-adik tamsayidir."""
from fractions import Fraction

K = 64
M = 1 << K

def from_rat(q, K=K):
    """Tek paydali rasyoneli mod 2^K'ya indir."""
    q = Fraction(q)
    a, d = q.numerator, q.denominator
    assert d % 2 == 1, "payda tek olmali (2-adik tamsayi)"
    return (a * pow(d, -1, 1 << K)) % (1 << K)

def show(x, K=32, digits=None):
    """Sola sonsuz yaziyi '...' ile goster."""
    s = format(x % (1 << K), f'0{K}b')
    if digits: s = s[-digits:]
    return '…' + s

def norm2(x, K=K):
    """|x|_2 = 2^-v(x); x=0 (mod 2^K) ise 0 kabul."""
    x %= (1 << K)
    if x == 0: return 0.0
    v = (x & -x).bit_length() - 1
    return 2.0 ** (-v)

def periodic_tail(q, K=200):
    """Rasyonelin ikili yazisindaki son-periyodu bul (onperiyot, periyot)."""
    s = format(from_rat(q, K), f'0{K}b')[::-1]  # s[i] = i. hane
    for L in range(1, 80):
        tail = s[100:]
        if all(tail[i] == tail[i+L] for i in range(len(tail)-L)):
            return L
    return None

if __name__ == '__main__':
    ex = [-1, Fraction(-1,3), Fraction(1,3), Fraction(-1,7), Fraction(1,5), Fraction(-3,7)]
    for q in ex:
        print(f'{str(q):>6} = {show(from_rat(q), 24)}   son periyot={periodic_tail(q)}')
    # Yasa testleri: halka islemleri rasyonellerde tutarli mi?
    import random
    random.seed(1)
    bad = 0
    for _ in range(20000):
        a = Fraction(random.randint(-999,999), random.randrange(1,999,2))
        b = Fraction(random.randint(-999,999), random.randrange(1,999,2))
        for op in (lambda u,v:u+v, lambda u,v:u*v, lambda u,v:u-v):
            if from_rat(op(a,b)) != op(from_rat(a), from_rat(b)) % M: bad += 1
    print('halka homomorfizmi hatasi (20000 cift x 3 islem):', bad)
    # -1 = ...111: x + (~x) = -1  (tum hanelerin tumleyeni)
    bad = sum(1 for x in range(1, 1<<14) if (x + ((~x) % M)) % M != M-1)
    print('x + tumleyen(x) = -1 hatasi (x<2^14):', bad)
    # 1/(1-2) = 1+2+4+... = -1 ; Sum 4^i = -1/3
    print('Σ 2^i (i<64) mod 2^64 == -1 :', sum(1<<i for i in range(64)) % M == from_rat(-1))
    print('Σ 4^i (i<32) mod 2^64 == -1/3:', sum(1<<(2*i) for i in range(32)) % M == from_rat(Fraction(-1,3)))
    # norm: |2^k|=2^-k, ultrametrik: |x+y| <= max
    bad = 0
    for _ in range(20000):
        x, y = random.randrange(1, M), random.randrange(1, M)
        if (x+y) % M and norm2(x+y) > max(norm2(x), norm2(y)): bad += 1
    print('ultrametrik esitsizlik hatasi (20000 cift):', bad)
    print('|2^10|_2 =', norm2(1<<10), ' |3|_2 =', norm2(3), ' 2^n -> 0 :', [norm2(1<<n) for n in (1,5,20)])
