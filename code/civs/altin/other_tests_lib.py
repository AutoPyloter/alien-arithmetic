import math
from sieve import mr
F = [1, 2]
while F[-1] < 10**20: F.append(F[-1] + F[-2])
def val(s): return sum(F[i] for i, c in enumerate(reversed(s)) if c == '1')
def zeck(n):
    s = []
    for f in reversed(F):
        if f <= n: s.append('1'); n -= f
        else: s.append('0')
    return ''.join(s).lstrip('0') or '0'
def pals(L):
    h = (L + 1) // 2; out = []
    def rec(s):
        if len(s) == h:
            if L % 2 == 0:
                if s[-1] == '1' and L > 1: return
                full = s + s[::-1]
            else: full = s + s[-2::-1]
            out.append(full); return
        for c in '01':
            if c == '1' and s[-1] == '1': continue
            rec(s + c)
    rec('1'); return out
