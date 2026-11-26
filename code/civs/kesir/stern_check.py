"""Bagimsiz kontrol: Stern diatomik dizisi s(n), n < 2^26. m'nin ilk goruldugu satir r: 2^r <= n <= 2^(r+1)."""
import numpy as np, math
R = 26
s = np.zeros(2 ** R + 2, dtype=np.int32); s[1] = 1
for r in range(R - 1):
    lo, hi = 2 ** r, 2 ** (r + 1)
    k = np.arange(lo, hi)
    s[2 * k] = s[k]; s[2 * k + 1] = s[k] + s[k + 1]

phi = (1 + 5 ** .5) / 2
for m in (54, 1230, 3160, 4470, 43800, 44764):
    idx = np.nonzero(s == m)[0]
    n = idx.min(); r = int(math.floor(math.log2(n)))
    f = math.floor(math.log(math.sqrt(5) * m) / math.log(phi)) - 2
    print(f"m={m}: ilk n={n}, satir v={r}, f={f}, v-f={r-f}")
