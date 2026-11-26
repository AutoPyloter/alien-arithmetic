import numpy as np
N=100_000_000
s=np.zeros(N+200,bool); P=np.load('/home/claude/P.npy'); s[P]=True
def S(g):
    r=1.0; m=g
    for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
        if g%p==0: r*=(p-1)/(p-2)
    return r
c2=np.sum(s[P]&s[P+2])
print("g  gözlenen/ikiz  tahmin")
for g in [2,4,6,8,10,12,14,28,30,32,210,2310]:
    c=np.sum(s[P+g]); print(g, round(c/c2,3), round(S(g),3))
