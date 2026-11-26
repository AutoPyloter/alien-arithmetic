"""Duzgun 5-gen ve 17-gen insasi (Carlyle cemberleriyle), yalnizca line/circle/meet.

Carlyle cemberi: x^2 - s x + p = 0 denkleminin kokleri, capi (0,1)-(s,p)
olan cemberin x eksenini kestigi noktalardir. Gauss'un 17-gen cozumu
4 kat ic ice ikinci derece denkleme iner; her biri bir Carlyle cemberi.
"""
import sys, time
import sympy as sp
from machine import Machine, perp_bisector, midpoint

def setup(M):
    O = M.add(0, 0, "O"); U = M.add(1, 0, "U")
    xa = M.line(O, U)
    unit = M.circle(O, U)
    Um = [P for P in M.meet(unit, xa, "U'") if P is not U][0]          # (-1,0)
    ya = perp_bisector(M, U, Um)                                         # y ekseni
    A = max(M.meet(unit, ya, "A"), key=lambda P: P.ny)                  # (0,1)
    return O, U, xa, ya, unit, A

def vertical_through(M, S, O, xa):
    """x ekseninde S'den gecen dik dogru."""
    if abs(S.nx) < 1e-30:
        raise ValueError
    S2 = [P for P in M.meet(M.circle(S, O), xa, "S2") if P is not O][0]  # (2s,0)
    return perp_bisector(M, O, S2)

def to_y_axis(M, P, O, ya, sign):
    """x eksenindeki (p,0) noktasini (0,p)'ye tasi (cember ile)."""
    pts = M.meet(M.circle(O, P), ya, "ty")
    return max(pts, key=lambda Q: sign * Q.ny)

def horizontal_through(M, T, O, ya):
    T2 = [P for P in M.meet(M.circle(T, O), ya, "T2") if P is not O][0]
    return perp_bisector(M, O, T2)

def carlyle(M, env, S, Pp, name):
    """x^2 - s x + p = 0 koklerini x ekseninde nokta olarak insa et."""
    O, U, xa, ya, unit, A = env
    sgn = 1 if Pp.nx > 0 else -1
    T = to_y_axis(M, Pp, O, ya, sgn)                 # (0,p)
    B = M.meet(vertical_through(M, S, O, xa), horizontal_through(M, T, O, ya), "B")[0]  # (s,p)
    C = midpoint(M, A, B, "mid")
    r = M.meet(M.circle(C, A), xa, name)
    return sorted(r, key=lambda P: P.nx)             # (kucuk, buyuk)

def neg_point(M, P, O, xa):
    return [Q for Q in M.meet(M.circle(O, P), xa, "neg") if Q is not P][0]

def vertices_from_cos(M, env, C2, n, name):
    """2cos(2pi/n) noktasindan duzgun n-gen kose noktalari."""
    O, U, xa, ya, unit, A = env
    c = midpoint(M, O, C2, "cos")
    P1 = max(M.meet(vertical_through(M, c, O, xa), unit, name + "1"), key=lambda P: P.ny)
    V = [U, P1]
    for k in range(2, n):
        nxt = [P for P in M.meet(M.circle(V[-1], V[-2]), unit, f"{name}{k}") if P is not V[-2]][0]
        V.append(nxt)
    return V

def pentagon(verbose=True):
    M = Machine(verbose=verbose)
    env = setup(M); O, U, xa, ya, unit, A = env
    m1 = neg_point(M, U, O, xa)                       # -1
    # x^2 + x - 1 = 0 -> kokler 2cos72, 2cos144
    r = carlyle(M, env, m1, m1, "r")
    V = vertices_from_cos(M, env, r[1], 5, "V")
    return M, V

def heptadecagon(verbose=True):
    M = Machine(verbose=verbose)
    env = setup(M); O, U, xa, ya, unit, A = env
    m1 = neg_point(M, U, O, xa)
    # -4: cember (O,U) ile 2'yi, sonra 4'u yap
    two = [P for P in M.meet(M.circle(U, O), xa, "2") if P is not O][0]
    four = [P for P in M.meet(M.circle(two, O), xa, "4") if P is not O][0]
    m4 = neg_point(M, four, O, xa)
    y2, y1 = carlyle(M, env, m1, m4, "y")             # x^2 + x - 4
    z2, z1 = carlyle(M, env, y1, m1, "z")             # x^2 - y1 x - 1
    w2, w1 = carlyle(M, env, y2, m1, "w")             # x^2 - y2 x - 1
    # 2cos(t), 2cos(4t): x^2 - z1 x + w1 = 0 ; w1 = 2(cos3t+cos5t)
    d = carlyle(M, env, z1, w1, "d")
    C2 = d[1]
    V = vertices_from_cos(M, env, C2, 17, "V")
    return M, V, (y1, y2, z1, z2, w1, w2, C2)

def report(M, V, n):
    import mpmath as mp
    ok = all(abs(V[k].nx - mp.cos(2 * mp.pi * k / n)) < 1e-60 and
             abs(V[k].ny - mp.sin(2 * mp.pi * k / n)) < 1e-60 for k in range(n))
    hist = {}
    for _, a, b in M.log:
        for d in (a, b): hist[d] = hist.get(d, 0) + 1
    print(f"{n}-gen: {n} kose dogru (60 basamak)={ok}; yeni nokta sayisi={len(M.points)}; "
          f"komut: {M.steps}; kule derinligi={M.T.n} ([K:Q]=2^{M.T.n})")
    print(f"   koordinat derecesi histogrami {dict(sorted(hist.items()))}; hepsi 2^k={all(d & (d-1) == 0 for d in hist)}")
    print(f"   V1: minpoly(cos) = {V[1].x.minpoly().as_expr()}")
    print(f"       deg sin = {V[1].y.minpoly().degree()}")
    print(f"   radikandlar (sayisal): {[float(r.val()) for r in M.T.rad[1:]]}")

if __name__ == "__main__":
    t = time.time()
    M, V = pentagon(verbose="-v" in sys.argv)
    report(M, V, 5)
    print(f"  sure {time.time()-t:.1f}s"); t = time.time()
    M, V, vals = heptadecagon(verbose="-v" in sys.argv)
    report(M, V, 17)
    print("  2cos(2pi/17) minimal polinomu:", vals[-1].x.minpoly().as_expr())
    print(f"  sure {time.time()-t:.1f}s")
