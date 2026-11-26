"""Kuzen uygarliklar: origami (Huzita-Hatori O6 / Beloch katlamasi) ve isaretli cetvel (neusis).

Hepsi sympy ile kesin; sayisal kontroller mpmath 50 basamak.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
x, t = sp.symbols('x t', real=True)


def reflect(P, A, B):
    """P noktasinin A-B dogrusuna gore yansimasi."""
    d = B - A
    proj = A + d * ((P - A).dot(d) / d.dot(d))
    return 2 * proj - P


def O6(p1, l1, p2, l2):
    """p1'i l1 dogrusuna, p2'yi l2 dogrusuna ayni anda goturen katlamalar.
    l = (Q, v): Q + s v.  q1 = Q1 + t v1 (p1'in goruntusu). Katlama dogrusu
    p1-q1'in orta dikmesidir. Kosul: p2'nin yansimasi l2 uzerinde. -> t icin polinom."""
    Q1, v1 = l1
    Q2, v2 = l2
    q1 = Q1 + t * v1
    M = (p1 + q1) / 2
    n = q1 - p1                         # katlama dogrusu n'ye dik, M'den gecer
    dirv = sp.Matrix([-n[1], n[0]])
    r = reflect(p2, M, M + dirv)
    cond = sp.together((r - Q2)[0] * v2[1] - (r - Q2)[1] * v2[0])
    num = sp.factor(sp.numer(cond))
    return num, (M, dirv, q1)


def abe(theta_deg=60):
    print(f"== Abe (1980) ucleme, aci {theta_deg} derece ==")
    th = sp.rad(theta_deg)
    h = sp.Rational(1, 4)
    B = sp.Matrix([0, 0]); E = sp.Matrix([0, 2 * h]); G = sp.Matrix([0, h])
    lBP = (B, sp.Matrix([sp.cos(th), sp.sin(th)]))
    lGH = (G, sp.Matrix([1, 0]))
    poly, (M, dirv, q1) = O6(E, lBP, B, lGH)          # E -> BP, B -> GH
    print("  O6 kosulu (t'de polinom):", sp.factor(poly))
    sols = [s for s in sp.Poly(poly, t).nroots(n=40) if s.is_real]
    for s in sols:
        Mn = M.subs(t, s); dn = dirv.subs(t, s)
        Bp = reflect(B, Mn, Mn + dn); Gp = reflect(G, Mn, Mn + dn)
        aB = sp.N(sp.atan2(Bp[1], Bp[0]) * 180 / sp.pi, 15)
        aG = sp.N(sp.atan2(Gp[1], Gp[0]) * 180 / sp.pi, 15)
        print(f"  t={sp.N(s, 12)}: B' yonu {aB} derece, G' yonu {aG} derece")
    tp = sp.Poly(poly, t)
    for f, e in sp.factor_list(tp)[1]:
        print("  carpan:", f.as_expr(), " derece", f.degree())


def messer():
    print("\n== Beloch/Messer: kup kok 2 ==")
    # parabol 1: odak (0,1), dogrultman y=-1 ;  parabol 2: odak (2,0), dogrultman x=-2
    p1 = sp.Matrix([0, 1]); l1 = (sp.Matrix([0, -1]), sp.Matrix([1, 0]))
    p2 = sp.Matrix([2, 0]); l2 = (sp.Matrix([-2, 0]), sp.Matrix([0, 1]))
    poly, (M, dirv, q1) = O6(p1, l1, p2, l2)
    print("  O6 kosulu:", sp.factor(poly))
    for f, e in sp.factor_list(sp.Poly(poly, t))[1]:
        print("    carpan:", f.as_expr())
    # katlama dogrusunun egimi
    for s in sp.Poly(poly, t).nroots(n=40):
        if s.is_real and abs(s) > 1e-30:
            slope = sp.N(dirv[1].subs(t, s) / dirv[0].subs(t, s), 30)
            print(f"  t={sp.N(s, 20)}  katlama egimi={slope}  egim^3={sp.N(slope**3, 25)}")
    print("  -> egim = -2^(1/3); derece 3, pergel-cetvelle imkansiz, katlamayla tek hamle.")


def archimedes(theta_deg=60):
    print(f"\n== Arsimet neusis uclemesi, aci {theta_deg} ==")
    th = mp.radians(theta_deg)
    A = (mp.cos(th), mp.sin(th))

    def F(d):  # D = (-d, 0); C = D + (A-D)/|A-D| ; |C|^2 - 1
        vx, vy = A[0] + d, A[1]
        n = mp.sqrt(vx * vx + vy * vy)
        cx, cy = -d + vx / n, vy / n
        return cx * cx + cy * cy - 1
    d = mp.findroot(F, 1.9)
    ang = mp.degrees(mp.atan2(A[1], A[0] + d))
    print(f"  isaretli cetvel kosulu |CD|=1 -> d = {mp.nstr(d, 30)}")
    print(f"  2cos(20) = {mp.nstr(2 * mp.cos(mp.radians(20)), 30)}")
    print(f"  ADO acisi = {mp.nstr(ang, 30)} derece")
    # kesin: d = 2cos(theta/3) kosulu saglar mi? cebirsel kanit: polinom
    dd = sp.Symbol('d', positive=True)
    c, s = sp.Rational(1, 2), sp.sqrt(3) / 2
    # C = D + u, |u|=1, u || (A-D); |C|=1 <=> |D|^2 + 2 D.u + 1 = 1 <=> d^2 - 2 d u_x = 0 <=> u_x = d/2
    # u_x = (c + d)/|A-D|  -> (c+d)^2 = (d/2)^2 ((c+d)^2 + s^2)
    eq = sp.expand((c + dd) ** 2 * 4 - dd ** 2 * ((c + dd) ** 2 + s ** 2))
    print("  kosul polinomu:", sp.factor(eq))
    print("  minpoly(2cos20) =", sp.minimal_polynomial(2 * sp.cos(sp.pi / 9), sp.Symbol('y')))


def polygons_table(N=100):
    print(f"\n== Duzgun n-gen tablosu, 3 <= n <= {N} ==")
    def fermat_ok(n):
        while n % 2 == 0: n //= 2
        for p in (3, 5, 17, 257, 65537):
            if n % p == 0:
                n //= p
                if n % p == 0: return False
        return n == 1
    def pierpont(p):
        q = p - 1
        while q % 2 == 0: q //= 2
        while q % 3 == 0: q //= 3
        return q == 1
    def origami_ok(n):
        for p, e in sp.factorint(n).items():
            if p in (2, 3): continue
            if e > 1 or not pierpont(p): return False
        return True
    def pow2(k): return k & (k - 1) == 0
    def totient_ok(n):  # phi(n) = 2^a 3^b (origami icin denk kosul)
        f = int(sp.totient(n))
        while f % 2 == 0: f //= 2
        while f % 3 == 0: f //= 3
        return f == 1
    comp = [n for n in range(3, N + 1) if fermat_ok(n)]
    ori = [n for n in range(3, N + 1) if origami_ok(n)]
    bad1 = [n for n in range(3, 10 ** 5) if fermat_ok(n) != pow2(int(sp.totient(n)))]
    bad2 = [n for n in range(3, 20001) if origami_ok(n) != totient_ok(n)]
    print("  pergel-cetvel:", comp)
    print("  origami     :", ori)
    print("  yalnizca origami:", [n for n in ori if n not in comp])
    print(f"  kontrol: 'n = 2^k x farkli Fermat asallari' <=> 'phi(n) 2^m'  (n<10^5) ihlal: {len(bad1)}")
    print(f"  kontrol: origami kosulu <=> 'phi(n) = 2^a 3^b'  (n<=20000) ihlal: {len(bad2)}")
    # neusis: p-gen (p asal) icin gerekli kosul p-1'in 5'ten buyuk asal boleni yok
    neu_need = [p for p in sp.primerange(3, N + 1) if max(sp.factorint(p - 1)) <= 5]
    print("  neusis icin GEREKLI (yeterli degil) kosulu saglayan asal p:", neu_need)
    print("  bunlardan origami ile olmayanlar:", [p for p in neu_need if not origami_ok(p)],
          "(11 Benjamin-Snyder 2014 ile cozuldu; 31, 41, 61 acik)")


if __name__ == "__main__":
    abe(60); abe(75)
    messer()
    archimedes(60)
    polygons_table(100)
