import sympy as sp
# (1) 3 tırmanışlı sistem
L1,L2,L3,e1,e2,e3=sp.symbols('L1 L2 L3 e1 e2 e3',positive=True,integer=True)
u1,u2,u3=sp.symbols('u1 u2 u3')
A=[3**L1*u1-2**(e1+L2)*u2-(1-2**e1),
   3**L2*u2-2**(e2+L3)*u3-(1-2**e2),
   3**L3*u3-2**(e3+L1)*u1-(1-2**e3)]
sol=sp.solve(A,[u1,u2,u3],dict=True)[0]
M=sp.Matrix([[3**L1,-2**(e1+L2),0],[0,3**L2,-2**(e2+L3)],[-2**(e3+L1),0,3**L3]])
print("det =",sp.simplify(M.det()))
for k,v in sol.items():
    num,den=sp.fraction(sp.together(v)); print(k,"=",sp.simplify(num),"/",sp.simplify(den))
# sayısal doğrulama: rastgele parametrelerle denklemleri sağla
import random
for _ in range(3):
    s={L1:random.randint(1,6),L2:random.randint(1,6),L3:random.randint(1,6),e1:random.randint(1,6),e2:random.randint(1,6),e3:random.randint(1,6)}
    vals={k:v.subs(s) for k,v in sol.items()}
    print([sp.simplify(eq.subs(s).subs(vals)) for eq in A])
