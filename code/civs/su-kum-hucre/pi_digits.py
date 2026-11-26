"""pi'nin ilk 10^6 ondalik basamagini mpmath ile hesaplayip dosyaya yazar."""
import sys, time, mpmath
sys.set_int_max_str_digits(0)
N = 10**6
t = time.time()
mpmath.mp.dps = N + 20
s = mpmath.nstr(mpmath.pi, N + 10, strip_zeros=False)
d = s.replace('.', '')[1:N + 1]   # '3' disindaki ilk N ondalik basamak
open('pi_1e6.txt', 'w').write(d)
print(len(d), d[:20], d[-10:], f"{time.time()-t:.1f}s")
