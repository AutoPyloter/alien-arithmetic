import json, time
bad=json.load(open('g11_bad.json')); t=time.time(); cnt=0; sols=[]
for L,K,_ in bad:
    S=K-L; D=2**K-3**L
    for L1 in range(1,L-1):
        for L2 in range(1,L-L1):
            L3=L-L1-L2
            for e1 in range(1,S-1):
                for e2 in range(1,S-e1):
                    e3=S-e1-e2; cnt+=1
                    N=(2**e1-1)*3**(L2+L3)+(2**e2-1)*2**(e1+L2)*3**L3+(2**e3-1)*2**(e1+e2+L2+L3)
                    if N%D: continue
                    u=[N//D]; Ls=[L1,L2,L3]; es=[e1,e2,e3]; good=u[0]%2==1
                    for i in range(2):
                        num=3**Ls[i]*u[i]+(2**es[i]-1); den=2**(es[i]+Ls[i+1])
                        if num%den: good=False; break
                        u.append(num//den); good&=u[-1]%2==1
                    if good: sols.append((Ls,es,[2**Ls[i]*u[i]-1 for i in range(3)]))
print("taranan altılı:",cnt,"süre %.0fs"%(time.time()-t))
print("çözümler:",sols)
