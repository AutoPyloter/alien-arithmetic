"""Görev 2: n<=N içinde kaç köklü / köksüz ağaç şekli görünür."""
import sys; sys.path.insert(0,'/home/claude/civs/agac-oyun')
from matula import tree, number, unrooted_canon, V
from sympy import prime
import collections
N = 10**6 if len(sys.argv)<3 else int(sys.argv[2])
# elek: en küçük asal bölen + asal indeksi
spf = list(range(N+1)); 
for i in range(2,int(N**.5)+1):
    if spf[i]==i:
        for j in range(i*i,N+1,i):
            if spf[j]==j: spf[j]=i
pidx = [0]*(N+1); c=0
for i in range(2,N+1):
    if spf[i]==i: c+=1; pidx[i]=c
Vs=[0,1]+[0]*(N-1)
for n in range(2,N+1):
    p=spf[n]; Vs[n]=Vs[n//p]+Vs[pidx[p]]   # V(pm)=V(m)+V(p_i)-1, V(p_i)=1+V(i)
A000081=[0,1,1,2,4,9,20,48,115,286,719,1842,4766,12486,32973,87811,235381]
A000055=[1,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320]
cnt=collections.Counter(Vs[1:]); first={}; last={}
for n in range(1,N+1):
    k=Vs[n]; first.setdefault(k,n); last[k]=n
print("k | n<=1e6 köklü | A000081 | ilk Matula | son Matula")
for k in range(1,17):
    full = prime(prime(1)) if False else None
    print(k, cnt[k], A000081[k], first.get(k), last.get(k))
# en büyük Matula (zincir) k köşe: tüm k-köşeli ağaçlar en geç zincirde tamamlanır
ch=[1]
for _ in range(8): ch.append(int(prime(ch[-1])))
print("zincir (en büyük) Matula:", ch)
# köksüz: n<=M için minimum köklemeli n'ler
M=int(sys.argv[1]) if len(sys.argv)>1 else 3000
uc=collections.Counter(); ufirst={}
for n in range(1,M+1):
    if unrooted_canon(tree(n))==n:
        k=Vs[n]; uc[k]+=1; ufirst.setdefault(k,n)
print("k | köksüz kanonik n<=",M,"| A000055 | ilk")
for k in range(1,14): print(k, uc[k], A000055[k], ufirst.get(k))
print("ilk köksüz kanonik numaralar:", [n for n in range(1,80) if unrooted_canon(tree(n))==n])
