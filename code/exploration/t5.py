import math
from fractions import Fraction
l2,l3=math.log(2),math.log(3)
# Baker tablosu: a^x ile b^y'nin yükseklik farkı, komşu olmak için gereken
print("x y  |x·h(a)-y·h(b)|  komşuluk için gereken ~1/min")
best=10
for y in range(1,60):
    x=round(y*l3/l2)
    d=abs(x*l2-y*l3)
    if d<best:
        best=d; need=1/min(2**x,3**y)
        print(x,y,"%.2e"%d,"%.2e"%need, "KOMŞU" if abs(2**x-3**y)==1 else "")
# log2(3) sürekli kesir yaklaşımları -> Collatz döngü adayları
x=Fraction(l3/l2).limit_denominator(10**12)
a=[];v=l3/l2
for _ in range(12): a.append(int(v)); v=1/(v-int(v))
print("log2(3) sürekli kesir:",a)
h0,h1,k0,k1=1,a[0],0,1
for t in a[1:]:
    h0,h1=h1,t*h1+h0; k0,k1=k1,t*k1+k0
    print("K/L =",h1,"/",k1, " 2^K-3^L işaret:", "+" if 2**h1>3**k1 else "-", " göreli fark %.1e"%abs(1-3**k1/2**h1))
# toplama = yumuşak max: h(u+w) vs max
for u,w in [(8,1),(100,99),(10**6,3)]:
    hu,hw=math.log(u),math.log(w); print(u,w,"h(u+w)=%.4f max=%.4f"%(math.log(u+w),max(hu,hw)))
