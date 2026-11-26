from sympy import factorint, primerange
L="abcdefghijklmnopqrstuvwxyz"
P=list(primerange(2,102))
def alien(n):
    if n==1: return "1"
    out=[]
    for p,e in sorted(factorint(n).items()):
        s=L[P.index(p)]
        if e>1:
            x=alien(e); s+= "^"+(x if len(x)==1 else "("+x+")")
        out.append(s)
    return ".".join(out)
for n in range(1,37): print(n, alien(n))
print("98",alien(98),"| 1000",alien(1000),"| 1024",alien(1024),"| 360",alien(360))
