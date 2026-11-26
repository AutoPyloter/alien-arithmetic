"""Geometri uygarligi: kesin pergel-cetvel cizim makinesi.

Yalnizca uc komut vardir:
  line(P, Q)      iki noktadan dogru (isaretsiz cetvel)
  circle(C, P)    merkez C, P'den gecen cember (Oklid'in "katlanan" pergeli)
  meet(A, B)      iki egrinin (dogru/cember) kesisim noktalari

Koordinatlar kesin cebirsel sayilardir (tower.py: ikinci dereceden kule).
Her yeni noktada x ve y'nin Q uzerindeki minimal polinomu kesin olarak
hesaplanir (kuvvetlerin Q-dogrusal bagimliligi, Fraction ile) ve derecenin 2'nin kuvveti oldugu kontrol edilir.
Karekok, ancak radikand mevcut cisimde kare degilse yeni bir seviye ekler.
"""
import mpmath as mp
import sympy as sp
from tower import Tower, E, minpoly_lin, support

TOL = mp.mpf(10) ** -60


class Point:
    def __init__(self, x, y, name=""):
        self.x, self.y, self.name = x, y, name

    @property
    def nx(self):
        return self.x.val()

    @property
    def ny(self):
        return self.y.val()

    def __repr__(self):
        return f"{self.name}({float(self.nx):.6f},{float(self.ny):.6f})"


class Line:  # a x + b y = c
    def __init__(self, P, Q):
        self.P, self.Q = P, Q
        self.a = Q.y - P.y
        self.b = P.x - Q.x
        self.c = self.a * P.x + self.b * P.y


class Circle:
    def __init__(self, C, P):
        self.C, self.P = C, P
        self.r2 = (P.x - C.x) * (P.x - C.x) + (P.y - C.y) * (P.y - C.y)


def is_pow2(d):
    return d >= 1 and d & (d - 1) == 0


class Machine:
    def __init__(self, check=True, verbose=False, cap=None):
        self.cap = cap            # destek > cap ise yalnizca kule sertifikasi (derece | 2^s)
        self.certified = 0        # kesin minpoly yerine kule sertifikasi kullanilan koordinat sayisi
        self.T = Tower()
        self.points, self.log, self.check, self.verbose = [], [], check, verbose
        self.steps = {"line": 0, "circle": 0}
        self.maxdeg = 1
        self._deg = {}

    def R(self, q):
        return E.rat(self.T, q)

    def degree(self, e):
        k = e.key()
        if self.cap is not None and k not in self._deg:
            sz = len(support(e))
            if sz > self.cap:
                self.certified += 1
                return -(1 << sz)          # negatif: 'derece 2^sz'yi boler' sertifikasi
        if k not in self._deg:
            self._deg[k] = len(minpoly_lin(e)) - 1   # (tower.E.minpoly ile capraz kontrol edildi)
        return self._deg[k]

    def add(self, x, y, name):
        if not isinstance(x, E): x = self.R(x)
        if not isinstance(y, E): y = self.R(y)
        P = Point(x, y, name)
        for Q in self.points:
            if abs(Q.nx - P.nx) < TOL and abs(Q.ny - P.ny) < TOL:
                assert (Q.x - P.x).is_zero() and (Q.y - P.y).is_zero()   # kesin esitlik
                return Q
        self.points.append(P)
        if self.check:
            dx, dy = self.degree(x), self.degree(y)
            assert is_pow2(abs(dx)) and is_pow2(abs(dy)), (name, dx, dy)
            self.maxdeg = max(self.maxdeg, dx, dy)
            self.log.append((name, dx, dy))
            if self.verbose:
                print(f"  {name:>6}: deg x={dx:<3} deg y={dy:<3} ({float(P.nx):+.6f}, {float(P.ny):+.6f})  kule={self.T.n}")
        return P

    def line(self, P, Q):
        self.steps["line"] += 1
        return Line(P, Q)

    def circle(self, C, P):
        self.steps["circle"] += 1
        return Circle(C, P)

    def meet(self, A, B, name="P"):
        if isinstance(A, Circle) and isinstance(B, Line):
            A, B = B, A
        if isinstance(A, Line) and isinstance(B, Line):
            det = A.a * B.b - A.b * B.a
            if det.is_zero():
                return []
            return [self.add((A.c * B.b - A.b * B.c) / det, (A.a * B.c - A.c * B.a) / det, name)]
        if isinstance(A, Circle) and isinstance(B, Circle):
            L = Line.__new__(Line)          # kok ekseni (iki cember denkleminin farki)
            L.a = (B.C.x - A.C.x) * 2
            L.b = (B.C.y - A.C.y) * 2
            L.c = (A.r2 - B.r2) + (B.C.x * B.C.x + B.C.y * B.C.y) - (A.C.x * A.C.x + A.C.y * A.C.y)
            if L.a.is_zero() and L.b.is_zero():
                return []
            return self._line_circle(L, A, name)
        return self._line_circle(A, B, name)

    def _line_circle(self, L, C, name):
        a, b, c = L.a, L.b, L.c
        if not b.is_zero():
            p0 = (self.R(0), c / b)
        else:
            p0 = (c / a, self.R(0))
        dx, dy = -b, a
        ux, uy = p0[0] - C.C.x, p0[1] - C.C.y
        A2 = dx * dx + dy * dy
        B1 = (ux * dx + uy * dy) * 2
        C0 = ux * ux + uy * uy - C.r2
        disc = B1 * B1 - A2 * C0 * 4
        if disc.is_zero():
            t = -B1 / (A2 * 2)
            return [self.add(p0[0] + t * dx, p0[1] + t * dy, name)]
        if disc.val() < 0:
            return []
        s = disc.sqrt()
        pts = []
        for t in ((-B1 - s) / (A2 * 2), (-B1 + s) / (A2 * 2)):
            pts.append(self.add(p0[0] + t * dx, p0[1] + t * dy, name))
        pts.sort(key=lambda P: (P.nx, P.ny))
        return pts


# ---- makrolar: hepsi yalnizca line/circle/meet kullanir ----
def perp_bisector(M, A, B):
    P, Q = M.meet(M.circle(A, B), M.circle(B, A), "aux")
    return M.line(P, Q)


def midpoint(M, A, B, name="mid"):
    return M.meet(perp_bisector(M, A, B), M.line(A, B), name)[0]
