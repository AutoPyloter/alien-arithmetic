from itertools import combinations
def cycles(K,L,sign):
    # 3n+sign döngüsü: n*(2^K-3^L) = sign * sum 3^(L-1-i) 2^(k_i)
    D=2**K-3**L; out=set()
    for ks in combinations(range(1,K),L-1):
        k=(0,)+ks
        S=sum(3**(L-1-i)*2**k[i] for i in range(L))*sign
        if D!=0 and S%D==0 and S//D>0:
            n=S//D
            # doğrula
            m=n; ok=True; odd=0; half=0
            for _ in range(K+L):
                if m%2: m=3*m+sign; odd+=1
                else: m//=2; half+=1
                if m==n: break
            if m==n and odd==L and half==K: out.add(n)
    return sorted(out)
for K,L in [(2,1),(8,5),(3,2),(11,7),(19,12),(5,3),(13,8)]:
    print(K,L,"3n+1:",cycles(K,L,1),"3n-1:",cycles(K,L,-1))
