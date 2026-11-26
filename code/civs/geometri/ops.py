"""Geometri uygarliginin temel islemleri: her biri yalnizca line/circle/meet ile.

Verilen noktalar: O = 0, U = 1. Girdi: z, w noktalari.
Her algoritma kesin olarak dogrulanir (sonuc = beklenen kesin deger) ve
kac pergel/cetvel komutu harcadigi sayilir.
"""
import random
from fractions import Fraction
from machine import Machine, Line, Circle, perp_bisector, midpoint


class Geo:
    def __init__(self, M):
        self.M = M
        self.O = M.add(0, 0, "O"); self.U = M.add(1, 0, "U")
        self.xa = M.line(self.O, self.U)
        self.unit = M.circle(self.O, self.U)
        self.Um = self.other(M.meet(self.unit, self.xa, "-1"), self.U)
        self.ya = perp_bisector(M, self.U, self.Um)

    @staticmethod
    def other(pts, P):
        r = [Q for Q in pts if Q is not P]
        return r[0] if r else P

    def on_real(self, P):
        return P.y.is_zero()

    # --- 1 komutluk islemler ---
    def abs(self, z):
        """|z|: igne 0'da, kalem z'de, cember; pozitif gercek ekseni kestigi yer."""
        return max(self.M.meet(self.M.circle(self.O, z), self.xa, "|z|"), key=lambda P: P.nx)

    def neg(self, z):
        """-z: O-z dogrusu ve O merkezli z'den gecen cember."""
        if z.x.is_zero() and z.y.is_zero(): return z
        return self.other(self.M.meet(self.M.circle(self.O, z), self.M.line(self.O, z), "-z"), z)

    def conj(self, z):
        """z eslenigi: O ve U merkezli, z'den gecen iki cemberin ikinci kesisimi."""
        if self.on_real(z): return z
        return self.other(self.M.meet(self.M.circle(self.O, z), self.M.circle(self.U, z), "zbar"), z)

    def double(self, z):
        """2z: z merkezli O'dan gecen cember, O-z dogrusu."""
        return self.other(self.M.meet(self.M.circle(z, self.O), self.M.line(self.O, z), "2z"), self.O)

    def mean(self, z, w):
        """(z+w)/2: orta dikme ile z-w dogrusunun kesisimi."""
        if (z.x - w.x).is_zero() and (z.y - w.y).is_zero(): return z
        return midpoint(self.M, z, w, "ort")

    def add(self, z, w):
        """z+w = 2*ortalama: m = (z+w)/2, sonra O'nun m'ye gore simetrigi."""
        if (z.x - w.x).is_zero() and (z.y - w.y).is_zero(): return self.double(z)
        m = self.mean(z, w)
        if m.x.is_zero() and m.y.is_zero(): return m
        return self.double(m)

    def sub(self, z, w):
        return self.add(z, self.neg(w))

    def rot90(self, z):
        """i*z: O'da O-z'ye dik dogru, O merkezli z'den gecen cember."""
        zm = self.neg(z)
        L = perp_bisector(self.M, z, zm)
        pts = self.M.meet(self.M.circle(self.O, z), L, "iz")
        # i*z = (-y, x): yon kontrolu yalnizca hangi kesisimin alinacagini secer
        return max(pts, key=lambda P: -P.nx * z.ny + P.ny * z.nx)

    def unitdir(self, z):
        """z/|z|: birim cember ile O-z isini."""
        pts = self.M.meet(self.unit, self.M.line(self.O, z), "e^ia")
        return max(pts, key=lambda P: P.nx * z.nx + P.ny * z.ny)

    def bisector_dir(self, a, b):
        """Iki birim yonun aci ortaypayi dogrusu (O'dan gecer)."""
        s = self.mean(a, b)
        if s.x.is_zero() and s.y.is_zero():      # zit yonler: dik dogru
            return perp_bisector(self.M, a, b)
        return self.M.line(self.O, s)

    def reflect(self, P, L):
        """P'nin L dogrusuna gore yansimasi (L.P, L.Q merkezli iki cember)."""
        A, B = L.P, L.Q
        return self.other(self.M.meet(self.M.circle(A, P), self.M.circle(B, P), "refl"), P)

    def real_mul(self, a, b):
        """Gercek a,b > 0 (x ekseninde): Tales (kesen) teoremi. Ikinci dogru: y ekseni."""
        Bp = max(self.M.meet(self.M.circle(self.O, b), self.ya, "b'"), key=lambda P: P.ny)  # (0,b)
        # U-B' dogrusuna A'dan paralel: X = A + B' - U
        X = self.sub(self.add(a, Bp), self.U)
        L = self.M.line(a, X)
        P = self.M.meet(L, self.ya, "ab'")[0]                                              # (0, ab)
        return max(self.M.meet(self.M.circle(self.O, P), self.xa, "ab"), key=lambda Q: Q.nx)

    def mul(self, z, w):
        """z*w: modul carpilir (Tales), acilar toplanir (U'yu acıortaya gore yansit)."""
        r = self.real_mul(self.abs(z), self.abs(w))
        ea, eb = self.unitdir(z), self.unitdir(w)
        L = self.bisector_dir(ea, eb)
        e = self.reflect(self.U, L)          # e^{i(a+b)}: U'nun aciortaya gore yansimasi
        pts = self.M.meet(self.M.circle(self.O, r), self.M.line(self.O, e), "zw")
        return max(pts, key=lambda P: P.nx * e.nx + P.ny * e.ny)

    def invert_circle(self, w):
        """Birim cembere gore evirtme w -> w/|w|^2 (yalniz pergel; |w|<=1/2 ise once ikiye katla)."""
        k = 0; v = w
        while 4 * (v.nx ** 2 + v.ny ** 2) <= 1:
            v = self.double(v); k += 1
        P, Q = self.M.meet(self.M.circle(v, self.O), self.unit, "PQ")
        s = self.other(self.M.meet(self.M.circle(P, self.O), self.M.circle(Q, self.O), "inv"), self.O)
        for _ in range(k):
            s = self.double(s)
        return s

    def inv(self, w):
        """1/w = eslenik(evirtme(w))."""
        return self.conj(self.invert_circle(w))

    def div(self, z, w):
        return self.mul(z, self.inv(w))

    def sqrt_real(self, r):
        """sqrt(r), r>0 gercek: capi [-1, r] olan cember y eksenini (0, sqrt r)'de keser."""
        c = self.mean(self.Um, r)
        Y = max(self.M.meet(self.M.circle(c, r), self.ya, "sqrt"), key=lambda P: P.ny)
        return max(self.M.meet(self.M.circle(self.O, Y), self.xa, "sqrt"), key=lambda P: P.nx)

    def sqrt(self, z):
        """sqrt z (esas dal): modulun karekoku + aci ikiye bolunur."""
        s = self.sqrt_real(self.abs(z))
        ez = self.unitdir(z)
        L = self.bisector_dir(self.U, ez)
        pts = self.M.meet(self.M.circle(self.O, s), L, "sqrtz")
        # esas dal: Re > 0, ya da Re = 0 ve Im >= 0
        return max(pts, key=lambda P: (P.nx, P.ny))


# ------------------------- testler -------------------------
def exact_expected(M, op, z, w):
    x1, y1 = z.x, z.y
    x2, y2 = (w.x, w.y) if w is not None else (None, None)
    if op == "add": return x1 + x2, y1 + y2
    if op == "sub": return x1 - x2, y1 - y2
    if op == "mul": return x1 * x2 - y1 * y2, x1 * y2 + y1 * x2
    if op == "div":
        n = x2 * x2 + y2 * y2
        return (x1 * x2 + y1 * y2) / n, (y1 * x2 - x1 * y2) / n
    if op == "inv":
        n = x1 * x1 + y1 * y1
        return x1 / n, -y1 / n
    if op == "conj": return x1, -y1
    if op == "neg": return -x1, -y1
    if op == "abs": return (x1 * x1 + y1 * y1).sqrt(), M.R(0)
    if op == "mean": return (x1 + x2) / 2, (y1 + y2) / 2
    if op == "rot90": return -y1, x1
    if op == "sqrt":
        r = (x1 * x1 + y1 * y1).sqrt()
        a = ((r + x1) / 2).sqrt()
        b = ((r - x1) / 2).sqrt()
        if y1.val() < 0: b = -b
        return a, b


def run_tests(trials=60, seed=7):
    random.seed(seed)
    ops = ["add", "sub", "mean", "neg", "conj", "abs", "rot90", "mul", "inv", "div", "sqrt"]
    stats = {op: [] for op in ops}
    fails = {op: 0 for op in ops}
    for tr in range(trials):
        M = Machine(check=False)
        G = Geo(M)
        def rnd():
            return Fraction(random.randint(-9, 9), random.randint(1, 4))
        zx, zy, wx, wy = rnd(), rnd(), rnd(), rnd()
        if zx == 0 and zy == 0: zx = Fraction(1, 2)
        if wx == 0 and wy == 0: wy = Fraction(3, 2)
        if tr % 3 == 2:   # bazen cebirsel (sqrt 2) girdiler
            z = M.add(M.R(zx) + M.R(2).sqrt(), M.R(zy), "z")
        else:
            z = M.add(zx, zy, "z")
        if tr % 4 == 3:   # kucuk |w|: evirtmede ikiye katlama dali
            wx, wy = Fraction(1, 5), Fraction(-1, 7)
        w = M.add(wx, wy, "w")
        for op in ops:
            before = dict(M.steps)
            f = getattr(G, op)
            res = f(z, w) if op in ("add", "sub", "mul", "div", "mean") else f(z)
            cost = (M.steps["line"] - before["line"]) + (M.steps["circle"] - before["circle"])
            ex, ey = exact_expected(M, op, z, w if op in ("add", "sub", "mul", "div", "mean") else None)
            ok = (res.x - ex).is_zero() and (res.y - ey).is_zero()
            if not ok: fails[op] += 1
            stats[op].append(cost)
    print(f"{'islem':<7} {'deneme':>6} {'hata':>5} {'komut (min-max)':>16}")
    for op in ops:
        print(f"{op:<7} {trials:>6} {fails[op]:>5} {min(stats[op]):>8}-{max(stats[op])}")
    return stats, fails


if __name__ == "__main__":
    run_tests()
