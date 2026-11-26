import numpy as np
from collections import Counter
N=100_000_000
s=np.ones(N+1,bool); s[:2]=False
for i in range(2,int(N**.5)+1):
    if s[i]: s[i*i::i]=False
P=np.nonzero(s)[0]; np.save('/home/claude/P.npy',P)
print("asal",len(P))
# 1 race mod 4
q=P[P>2]%4
d=np.cumsum(np.where(q==3,1,-1))
print("mod4: 3-sınıfı önde olduğu oran %",round(100*np.mean(d>0),4),"| 1-sınıfı önde ilk kez p=",P[P>2][np.argmax(d<0)] if (d<0).any() else None, "| son fark",d[-1])
q3=P[P>3]%3; d3=np.cumsum(np.where(q3==2,1,-1)); print("mod3: 2-sınıfı önde %",round(100*np.mean(d3>0),5),"ters ilk",P[P>3][np.argmax(d3<0)] if (d3<0).any() else None)
# 2 last digit pairs
L=P[P>5]%10
pairs=Counter(zip(L[:-1].tolist(),L[1:].tolist()))
tot=sum(pairs.values())
print("ardışık son basamak (beklenen %6.25):")
for a in [1,3,7,9]:
    print(a,[round(100*pairs[(a,b)]/tot,2) for b in [1,3,7,9]])
# 3 gaps
g=np.diff(P)
cg=Counter(g.tolist())
print("en sık boşluklar:",cg.most_common(6))
# Cramér: P(gap=k) random model with density 1/ln: compare ratio of gap 6 to gap 2 and 4
print("2:",cg[2],"4:",cg[4],"6:",cg[6],"30:",cg[30],"32:",cg[32],"28:",cg[28])
print("max gap",g.max(),"at",P[np.argmax(g)])
