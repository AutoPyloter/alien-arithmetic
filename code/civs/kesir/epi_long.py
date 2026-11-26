"""e+pi icin daha uzun SK (Khinchin sapmasi suruyor mu?)."""
import sys, time, numpy as np, mpmath as mp
from reals import cf_mp
D = int(sys.argv[1]); t = time.time()
cf = cf_mp(lambda: mp.e + mp.pi, D)
np.save('data/epi_long.npy', np.array(cf, dtype=object)); print(len(cf), f'{time.time()-t:.0f}s')
