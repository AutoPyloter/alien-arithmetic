import sys, random, time
sys.path.insert(0,'/home/claude/civs/agac-oyun')
from oyun import *
from fractions import Fraction
t0=time.time()
# 1. Sürreal doğum günleri
days = numbers_by_day(5)
print("gün başına yeni sayı:", [len(d) for d in days])
print("gün 2:", sorted(days[2]), " gün 3:", sorted(days[3]))
# oyun motoruyla: kurulan sürreal oyunlar sıralamaya uyuyor mu
nums = sorted(set().union(*days[:5]))
gs = [from_dyadic(x) for x in nums]
for i,x in enumerate(nums):
    for j,y in enumerate(nums):
        assert le(gs[i],gs[j]) == (x<=y)
# toplama: oyun toplamı = sayı toplamı
for x in nums[::3]:
    for y in nums[::3]:
        assert eq(add(from_dyadic(x),from_dyadic(y)), from_dyadic(x+y))
print("sürreal sıralama ve toplama OK, sayı adedi", len(nums))
# 2. tüm oyunlar
print("doğan oyun sınıfı sayısı gün 0,1,2:", [len(games_by_day(k)) for k in range(3)])
star = G([ZERO],[ZERO])
assert not le(star,ZERO) and not le(ZERO,star)   # * ile 0 karşılaştırılamaz
assert eq(add(star,star), ZERO)                  # *+* = 0
half = from_dyadic(Fraction(1,2)); assert eq(add(half,half), from_dyadic(1))
# 3. Hackenbush dizileri = Berlekamp değeri
from itertools import product
cnt=0
for n in range(0,9):
    for s in product('BR',repeat=n):
        s=''.join(s); assert eq(hack_game(s), from_dyadic(berlekamp(s))); cnt+=1
print("Hackenbush dizileri (uzunluk<=8):", cnt, "OK; ör. BRB =", berlekamp('BRB'), " BBR =", berlekamp('BBR'))
# 4. Sprague–Grundy: Nim toplamı = XOR
import itertools
nim = lambda h: range(1,h+1)
for hs in itertools.product(range(7),repeat=3):
    assert grundy_sum(hs,nim) == hs[0]^hs[1]^hs[2]
sub = lambda h: [m for m in (1,3,4) if m<=h]   # S={1,3,4} çıkarma oyunu
single=[grundy_sum((h,),sub) for h in range(30)]
print("S={1,3,4} Grundy dizisi:", single[:21])
for a in range(15):
    for b in range(15):
        assert grundy_sum((a,b),sub) == single[a]^single[b]
print("Sprague–Grundy (toplam=XOR) OK")
# 5. Nimber çarpımı
for a in range(32):
    for b in range(32):
        assert nim_mul_def(a,b) == nim_mul(a,b)
print("Conway tanımı = hızlı algoritma (a,b<32) OK")
print("nim çarpım tablosu 0..15:")
for a in range(16): print(' '.join(f"{nim_mul(a,b):2d}" for b in range(16)))
for F in (2,4,16,256):
    R=range(F)
    for a in R:
        for b in R:
            assert nim_mul(a,b) < F and nim_mul(a,b)==nim_mul(b,a)
    for a,b,c in [(random.randrange(F),random.randrange(F),random.randrange(F)) for _ in range(20000)] if F==256 else itertools.product(R,R,R):
        assert nim_mul(nim_mul(a,b),c)==nim_mul(a,nim_mul(b,c))
        assert nim_mul(a,b^c)==nim_mul(a,b)^nim_mul(a,c)
    for a in range(1,F): assert any(nim_mul(a,b)==1 for b in range(1,F))
    print(f"[0,{F}) cisim: kapalı, değişmeli, birleşmeli, dağılmalı, terslenir OK")
# Fermat kuralı ve Frobenius
for k in range(6):
    F=1<<(1<<k); assert nim_mul(F,F)==3*F//2
print("F⊗F=3F/2 OK; 2⊗2 =",nim_mul(2,2)," 4⊗4 =",nim_mul(4,4)," 16⊗16 =",nim_mul(16,16))
# 2^(2^k) altında x -> x^2 Frobenius toplamsal
for a in range(256):
    for b in range(256):
        assert nim_mul(a^b,a^b)==nim_mul(a,a)^nim_mul(b,b)
# çarpımsal grup döngüsel: 256'da üreteç
def order(a,F):
    x=a;k=1
    while x!=1: x=nim_mul(x,a);k+=1
    return k
print("[0,16) içinde mertebe 15 olan (üreteç) sayısı:", sum(order(a,16)==15 for a in range(1,16)))
print("[0,256) içinde üreteç sayısı:", sum(order(a,256)==255 for a in range(1,256)), "(φ(255)=128 beklenir)")
# Conway: ω^3 = 2 karşılığı sonlu: 4 = 2^(2^1)... küp kökler
print("x⊗x⊗x = 2 çözümleri <256:", [x for x in range(256) if nim_mul(nim_mul(x,x),x)==2])
print("süre",round(time.time()-t0,1))
