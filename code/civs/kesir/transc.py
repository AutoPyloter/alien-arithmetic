"""pi, e, e+pi, ln2, rastgele sayilar icin SK katsayilari (mpmath, aralik yontemi)."""
import sys, time, numpy as np, mpmath as mp
from reals import cf_mp
D = int(sys.argv[1]) if len(sys.argv) > 1 else 110000
for name, f in [('pi', lambda: mp.pi), ('e', lambda: mp.e), ('epi', lambda: mp.e + mp.pi),
                ('ln2', lambda: mp.log(2)), ('pi2', lambda: mp.pi**2)]:
    t = time.time()
    cf = cf_mp(f, D)
    np.save(f'data/{name}.npy', np.array(cf, dtype=object))
    print(name, len(cf), cf[:12], f'{time.time()-t:.1f}s', flush=True)
