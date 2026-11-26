import math, sympy as sp
phi=(1+5**.5)/2
F=[1,2]
while F[-1]<10**13: F.append(F[-1]+F[-2])   # F[0]=1,F[1]=2,3,5,8...
def zeck(n):
    bits=[]; 
    for f in reversed(F):
        if f<=n: bits.append(1); n-=f
        else: bits.append(0)
    s=''.join(map(str,bits)).lstrip('0'); return s or '0'
def val(s): return sum(F[i] for i,c in enumerate(reversed(s)) if c=='1')
# (a) +1 maliyeti: değişen hane sayısı
N=200000
ch_z=0; ch_b=0
for n in range(1,N):
    a=zeck(n).zfill(30); b=zeck(n+1).zfill(30); ch_z+=sum(x!=y for x,y in zip(a,b))
    ch_b+=bin(n^(n+1)).count('1')
print("+1'de değişen ortalama hane: altın %.3f, ikili %.3f"%(ch_z/N,ch_b/N))
# (b) kaydırma (×φ benzeri): shift(n) = val(zeck(n)+'0')
bad=[0,0,0]
for n in range(1,N):
    s=val(zeck(n)+'0')
    for k,c in enumerate([math.floor(n*phi), round(n*phi), math.floor((n+1)*phi)-1]):
        bad[k]+= (s!=c)
print("kaydırma = ⌊nφ⌋ hatası, round(nφ) hatası, ⌊(n+1)φ⌋−1 hatası:",bad)
# (c) Wythoff: ⌊nφ⌋ değerleri hangi Zeckendorf'larda
low=set(math.floor(n*phi) for n in range(1,N))
mis=0
for m in range(1,N):
    z=zeck(m); tz=len(z)-len(z.rstrip('0'))
    mis += ((m in low) != (tz%2==0))
print("alt Wythoff ⇔ sondaki sıfır sayısı çift: uyumsuz =",mis)
# (d) Knuth daire çarpımı a∘b = Σ F_{i+j+2?} : Zeckendorf indeksleri (F_2=1 tabanında)
def idx(n): z=zeck(n); return [len(z)-1-i for i,c in enumerate(z) if c=='1']  # 0 tabanlı: F[0]=1
def circ(a,b): return sum(F[i+j+2] for i in idx(a) for j in idx(b))
ok=all(circ(circ(a,b),c)==circ(a,circ(b,c)) for a in range(1,40) for b in range(1,40) for c in range(1,25))
print("Knuth çarpımı birleşmeli (a,b<40,c<25):",ok, " örnek 2∘3 =",circ(2,3),", 3∘3 =",circ(3,3))
