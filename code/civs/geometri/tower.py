"""Ikinci dereceden kule: Q = K0 < K1 = K0(sqrt d1) < K2 = K1(sqrt d2) < ...

Her eleman kesin olarak tutulur: K_k elemani = a + b*sqrt(d_k), a,b in K_{k-1}.
Yeni bir karekok yalnizca radikand mevcut cisimde KARE DEGILSE eklenir; bu
yuzden temsil tektir (sifir testi ve esitlik kesindir) ve [K_n : Q] = 2^n.

Minimal polinom: karakteristik polinom chi(X) = N_{K_n/Q}(X - alpha) kesin
olarak normlarla hesaplanir; chi = m^e oldugundan m = chi'nin karesiz kismi.
Derece = 2^n / e, her zaman 2'nin kuvveti -- ama burada gercekten hesaplanir.
"""
from fractions import Fraction
from math import isqrt
import mpmath as mp
import sympy as sp

mp.mp.dps = 90


class Tower:
    def __init__(self):
        self.rad = [None]      # rad[k] = d_k (K_{k-1} elemani)
        self.sv = [None]       # sqrt(d_k) sayisal degeri
        self.sq = {}           # karekok onbellegi

    @property
    def n(self):
        return len(self.rad) - 1


class E:
    """Kule elemani. lvl=0: Fraction q. lvl>0: a + b*sqrt(d_lvl)."""
    __slots__ = ("T", "lvl", "q", "a", "b", "_v")

    def __init__(self, T, lvl, q=None, a=None, b=None):
        self.T, self.lvl, self.q, self.a, self.b, self._v = T, lvl, q, a, b, None

    # --- yapim ---
    @staticmethod
    def rat(T, q):
        return E(T, 0, q=Fraction(q))

    def lift(self, lvl):
        x = self
        while x.lvl < lvl:
            x = E(self.T, x.lvl + 1, a=x, b=E.zero(self.T, x.lvl))
        return x

    @staticmethod
    def zero(T, lvl):
        return E.rat(T, 0).lift(lvl)

    def is_zero(self):
        if self.lvl == 0:
            return self.q == 0
        return self.a.is_zero() and self.b.is_zero()

    def low(self):
        x = self
        while x.lvl > 0 and x.b.is_zero():
            x = x.a
        return x

    # --- aritmetik ---
    def _co(self, o):
        if not isinstance(o, E):
            o = E.rat(self.T, o)
        L = max(self.lvl, o.lvl)
        return self.lift(L), o.lift(L)

    def __add__(self, o):
        if not isinstance(o, E):
            o = E.rat(self.T, o)
        x, y = self, o
        if x.lvl == 0 and y.lvl == 0:
            return E.rat(x.T, x.q + y.q)
        if x.lvl > y.lvl:
            return E(x.T, x.lvl, a=x.a + y, b=x.b)
        if y.lvl > x.lvl:
            return E(x.T, y.lvl, a=x + y.a, b=y.b)
        b = x.b + y.b
        a = x.a + y.a
        return a if b.is_zero() else E(x.T, x.lvl, a=a, b=b)
    __radd__ = __add__

    def __neg__(self):
        if self.lvl == 0:
            return E.rat(self.T, -self.q)
        return E(self.T, self.lvl, a=-self.a, b=-self.b)

    def __sub__(self, o):
        return self + (-o if isinstance(o, E) else E.rat(self.T, -Fraction(o)))

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, E):
            o = E.rat(self.T, o)
        x, y = self, o
        if x.lvl == 0 and y.lvl == 0:
            return E.rat(x.T, x.q * y.q)
        if x.lvl > y.lvl:
            if y.is_zero(): return y
            return E(x.T, x.lvl, a=x.a * y, b=x.b * y)
        if y.lvl > x.lvl:
            if x.is_zero(): return x
            return E(x.T, y.lvl, a=x * y.a, b=x * y.b)
        d = x.T.rad[x.lvl]
        a = x.a * y.a + d * (x.b * y.b)
        b = x.a * y.b + x.b * y.a
        return a if b.is_zero() else E(x.T, x.lvl, a=a, b=b)
    __rmul__ = __mul__

    def conj(self):
        return E(self.T, self.lvl, a=self.a, b=-self.b)

    def inv(self):
        if self.lvl == 0:
            return E.rat(self.T, 1 / self.q)
        d = self.T.rad[self.lvl]
        nrm = self.a * self.a - d * (self.b * self.b)
        ni = nrm.inv()
        if self.b.is_zero():
            return self.a.inv()
        return E(self.T, self.lvl, a=self.a * ni, b=-(self.b * ni))

    def __truediv__(self, o):
        if not isinstance(o, E):
            o = E.rat(self.T, o)
        return self * o.inv()

    # --- sayisal deger ---
    def val(self):
        if self._v is None:
            if self.lvl == 0:
                self._v = mp.mpf(self.q.numerator) / self.q.denominator
            else:
                self._v = self.a.val() + self.b.val() * self.T.sv[self.lvl]
        return self._v

    def key(self):
        if self.lvl == 0:
            return (self.q,)
        x = self.low()
        if x.lvl == 0:
            return (x.q,)
        return (x.lvl, x.a.key(), x.b.key())

    # --- karekok ---
    def sqrt_in(self, k=None):
        """K_k icinde (varsayilan: tum kule) karekok varsa dondur, yoksa None."""
        T = self.T
        if k is None:
            k = T.n
        if k == 0:
            D = self.low()
            assert D.lvl == 0
            q = D.q
            if q < 0:
                return None
            n, m = q.numerator, q.denominator
            rn, rm = isqrt(n), isqrt(m)
            if rn * rn == n and rm * rm == m:
                return E.rat(T, Fraction(rn, rm))
            return None
        ck = (self.key(), k)
        if ck in T.sq:
            return T.sq[ck]
        r = self._sqrt_in(k)
        T.sq[ck] = r
        return r

    def _sqrt_in(self, k):
        T = self.T
        D = self.low().lift(k)
        d = T.rad[k]
        a, b = D.a, D.b
        if b.is_zero():
            r = a.sqrt_in(k - 1)
            if r is not None:
                return r.lift(k)
            y = (a / d).sqrt_in(k - 1)
            if y is not None:
                return E(T, k, a=E.zero(T, k - 1), b=y)
            return None
        N = a * a - d * (b * b)
        n0 = N.sqrt_in(k - 1)
        if n0 is None:
            return None
        for s in (1, -1):
            x = ((a + n0 * s) / 2).sqrt_in(k - 1)
            if x is not None and not x.is_zero():
                y = b / (x * 2)
                return E(T, k, a=x.lift(k - 1), b=y.lift(k - 1))
        return None

    def sqrt(self):
        """Pozitif karekok; gerekirse kuleye yeni seviye ekle."""
        T = self.T
        assert self.val() >= 0
        if self.is_zero():
            return self
        r = self.sqrt_in()
        if r is None:
            D = self.lift(T.n)
            T.rad.append(D)
            T.sv.append(mp.sqrt(D.val()))
            r = E(T, T.n, a=E.zero(T, T.n - 1), b=E.rat(T, 1).lift(T.n - 1))
        if r.val() < 0:
            r = -r
        return r

    # --- minimal polinom ---
    def charpoly(self):
        """chi(X) = N(X - alpha), katsayilar Fraction, derece 2^lvl (en dusuk seviyede)."""
        x = self.low()
        P = [-x, E.rat(self.T, 1).lift(x.lvl)]      # X - alpha
        lvl = x.lvl
        while lvl > 0:
            d = self.T.rad[lvl]
            A = [c.lift(lvl).a for c in P]
            B = [c.lift(lvl).b for c in P]
            if all(b.is_zero() for b in B):   # bu seviye kullanilmiyor: atla
                P = A
                lvl -= 1
                continue
            AA = pmul(A, A)
            BB = pmul(B, B)
            P = [AA[i] - d * BB[i] for i in range(len(AA))]
            lvl -= 1
        return [c.low().q for c in P]

    def minpoly(self):
        X = sp.Symbol('x')
        chi = self.charpoly()
        p = sp.Poly(list(reversed([sp.Rational(c.numerator, c.denominator) for c in chi])), X, domain='QQ')
        m = sp.sqf_part(p)
        return m


def pmul(A, B):
    R = [None] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            t = a * b
            R[i + j] = t if R[i + j] is None else R[i + j] + t
    return R


# ---- daha hizli minimal polinom: kuvvetlerin Q-dogrusal bagimliligi ----
def support(x, acc=None):
    """x'in agacinda b != 0 olan seviyeler ve onlarin radikandlarinin destekleri."""
    if acc is None:
        acc = set()
    x = x.low()
    if x.lvl == 0:
        return acc
    if not x.b.is_zero() and x.lvl not in acc:
        acc.add(x.lvl)
        support(x.T.rad[x.lvl], acc)
    support(x.a, acc)
    support(x.b, acc)
    return acc


def flat(x, L):
    """x'in Q-taban vektoru; L: azalan sirali seviye listesi (kapanis)."""
    if not L:
        x = x.low()
        assert x.lvl == 0
        return [x.q]
    top = L[0]
    if x.lvl > top:
        assert x.b.is_zero()
        return flat(x.a, L)
    if x.lvl == top:
        return flat(x.a, L[1:]) + flat(x.b, L[1:])
    return flat(x, L[1:]) + [Fraction(0)] * (1 << (len(L) - 1))


def minpoly_lin(x):
    """Minimal polinom (monik, Fraction katsayilar, artan dereceler)."""
    L = sorted(support(x), reverse=True)
    rows = []          # (pivot, vektor, kombinasyon)
    p = E.rat(x.T, 1)
    k = 0
    while True:
        v = flat(p, L)
        comb = [Fraction(0)] * (k + 1); comb[k] = Fraction(1)
        for piv, rv, rc in rows:
            c = v[piv]
            if c != 0:
                v = [a - c * b for a, b in zip(v, rv)]
                comb = [a - c * (rc[i] if i < len(rc) else 0) for i, a in enumerate(comb)]
        nz = next((i for i, a in enumerate(v) if a != 0), None)
        if nz is None:
            return comb            # sum comb[i] x^i = 0, comb[k] = 1
        c = v[nz]
        rows.append((nz, [a / c for a in v], [a / c for a in comb]))
        p = p * x
        k += 1
