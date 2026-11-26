"""Aci ucleme: cebirsel kanit + cizim makinesiyle deneysel kontrol + kiris uclemesi."""
import random, sys, time
import sympy as sp
import mpmath as mp
from machine import Machine, Line, Circle

x = sp.Symbol('x')

def algebra():
    print("== 1. Cebir ==")
    t = sp.Symbol('t')
    ident = sp.simplify(sp.expand_trig(sp.cos(3 * t)) - (4 * sp.cos(t) ** 3 - 3 * sp.cos(t)))
    print("cos3t - (4cos^3 t - 3cos t) =", ident)
    f = 8 * x ** 3 - 6 * x - 1
    cands = sorted({sp.Rational(s * a, b) for s in (1, -1) for a in (1,) for b in (1, 2, 4, 8)})
    print("rasyonel kok adaylari (p|1, q|8):", cands)
    print("degerler:", [f.subs(x, c) for c in cands], "-> hicbiri 0 degil")
    print("Q uzerinde carpanlar:", sp.factor_list(f))
    print("minpoly(cos 20 derece) =", sp.minimal_polynomial(sp.cos(sp.pi / 9), x))
    print("derece 3; 3 ikinin kuvveti degil -> cos20 cizilemez.")
    # genel: hangi tamsayi derece acilar ucelenebilir? cos(theta/3) derecesi
    print("\n 360/n acisinin uclenebilmesi (n<=1000, n cizilebilir): uclenebilir <=> 3 n'yi bolmez")
    bad = 0; tested = 0
    for n in range(1, 1001):
        if not pow2(sp.totient(n)):
            continue
        tested += 1
        tris = pow2(sp.totient(3 * n))
        if tris != (n % 3 != 0):
            bad += 1
    print(f"   cizilebilir n<=1000: {tested} tane, kural ihlali: {bad}")

def pow2(d):
    d = int(d); return d & (d - 1) == 0

def chord():
    print("\n== 3. Kirisi uce bolmek ==")
    U = sp.Matrix([1, 0]); W = sp.Matrix([sp.Rational(1, 2), sp.sqrt(3) / 2])
    pts = [U + sp.Rational(k, 3) * (W - U) for k in range(4)]
    ang = [sp.atan2(P[1], P[0]) for P in pts]
    parts = [sp.N((ang[k + 1] - ang[k]) * 180 / sp.pi, 8) for k in range(3)]
    print("60 derece kirisi 3 esit parca -> acilar:", parts, " toplam", sum(parts))
    for k in (1, 2):
        P = pts[k]; c = sp.simplify(P[0] / sp.sqrt(P[0] ** 2 + P[1] ** 2))
        print(f"   bolum noktasi {k}: cos(aci) = {sp.nsimplify(c)}  derece {sp.degree(sp.minimal_polynomial(c, x))}")
    # kucuk acilarda hata: orta parca - theta/3 ~ ?
    th = sp.Symbol('th')
    a1 = sp.atan(sp.sin(th) / 3 / (1 - sp.Rational(1, 3) + sp.cos(th) / 3))
    mid = th - 2 * a1
    print("   kucuk theta icin dis parca =", sp.series(a1, th, 0, 6))
    print("   orta - dis =", sp.series(mid - a1, th, 0, 6))
    for deg in (30, 60, 90, 120, 150, 179):
        t = mp.radians(deg)
        A1 = mp.atan(mp.sin(t) / (2 + mp.cos(t)))
        print(f"   theta={deg:>3}: dis {float(mp.degrees(A1)):.4f}, orta {float(mp.degrees(t-2*A1)):.4f}")

def explore(seed=1, walks=400, depth=5):
    """60 derece baslangicindan rastgele derin insa yuruyusleri. Her yuruyus asama-1
    noktalarindan (12 nokta) baslar, 'depth' adim gider (her adim: en yeni noktayi
    kullanan bir egri ile rastgele bir egrinin kesisimi), sonra geri sarilir."""
    from stages import stage, Snapshot
    print("\n== 2b. Rastgele derin insalar (60 derece baslangici) ==")
    random.seed(seed)
    M = Machine(check=True)
    O = M.add(0, 0, "O"); U = M.add(1, 0, "U")
    W = M.add(M.R(1) / 2, M.R(3).sqrt() / 2, "W")
    stage(M, list(M.points), "s1")
    snap = Snapshot(M)
    hits = 0; steps = 0; npts = 0; maxdepth = 0; degs = {}
    t = time.time()
    for w in range(walks):
        for d in range(depth):
            P = M.points
            i = len(P) - 1
            j, k, l = (random.randrange(len(P)) for _ in range(3))
            if j == i: j = (i + 1) % len(P)
            if k == l: l = (k + 1) % len(P)
            c1 = (M.line if random.random() < .4 else M.circle)(P[i], P[j])
            c2 = (M.line if random.random() < .4 else M.circle)(P[k], P[l])
            b0 = len(M.points)
            M.meet(c1, c2, "Rw"); steps += 1
            for Q in M.points[b0:]:
                npts += 1
                for R_ in M.points:
                    if R_ is Q: continue
                    ang = mp.degrees(mp.atan2(Q.ny - R_.ny, Q.nx - R_.nx)) % 60
                    if min(abs(ang - 20), abs(ang - 40)) < 1e-40:
                        hits += 1
        maxdepth = max(maxdepth, M.T.n)
        for _, a, c in M.log[snap.log:]:
            for dd in (a, c): degs[dd] = degs.get(dd, 0) + 1
        snap.restore()
    print(f"{walks} yuruyus x {depth} adim = {steps} kesisim, {npts} yeni nokta, en derin kule {maxdepth}  ({time.time()-t:.0f}s)")
    print("yeni koordinat derecesi histogrami:", dict(sorted(degs.items())))
    print("hepsi 2^k:", all(dd & (dd - 1) == 0 for dd in degs), "; 3'e bolunen derece sayisi:",
          sum(v for dd, v in degs.items() if dd % 3 == 0))
    print("20/40 (mod 60) derecelik iki-nokta yonu bulundu mu:", hits)
    return M

if __name__ == "__main__":
    algebra(); chord()
    t = time.time(); explore(); print(f"sure {time.time()-t:.0f}s")
