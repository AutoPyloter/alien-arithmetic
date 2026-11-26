import math
from mpmath import mp, mpf, log, ceil
mp.dps=60
l2=log(2); l3=log(3); r=1/math.log2(3); kap=r**2*(1-r)/(1-r**3)
bad=[]
for L in range(3,86800):
    K=int(ceil(L*l3/l2)); 
    while True:
        d=K*l2-L*l3
        if d<=0: K+=1; continue
        if d< 6*mpf(2)**(-kap*L): bad.append((L,K,float(d)))
        else: break
        K+=1
print("ihlal mümkün L sayısı:",len(bad),"  en büyük L:",max(b[0] for b in bad) if bad else None)
print(sorted(set(b[0] for b in bad))[-15:])
import json; json.dump(bad,open('g11_bad.json','w'))
