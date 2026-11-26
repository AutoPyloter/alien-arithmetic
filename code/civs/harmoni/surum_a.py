"""Harmoni uygarligi, Surum A: s_n(t) = sum_p v_p(n) sin(2 pi p t).
Carpma = sinyal toplami; carpanlara ayirma = FFT ile spektrum okuma."""
import numpy as np, time, wave, math, json
from sympy import factorint, primerange, nextprime, randprime
rng = np.random.default_rng(1)

def signal(n, N=None):
    f = factorint(n)
    P = max(f) if f else 1
    if N is None: N = 2*P + 2          # Nyquist: ornek sayisi > 2*en buyuk asal
    t = np.arange(N)/N
    s = np.zeros(N)
    for p, e in f.items(): s += e*np.sin(2*np.pi*p*t)
    return s, N

def decode(s):
    N = len(s); X = np.fft.rfft(s)
    amp = -2*X.imag/N                   # sin genligi
    out = {}
    for p in primerange(2, N//2):
        e = int(round(amp[p]))
        if e > 0: out[p] = e
    return out

res = {}
# 1) Kayipsiz geri okuma
bad = 0
for n in range(2, 20001):
    s, N = signal(n)
    if decode(s) != factorint(n): bad += 1
res['exact_decode_2_20000_errors'] = bad
# 2) Carpma = toplama (ortak ornek sayisi ile)
bad = 0
for _ in range(2000):
    a, b = rng.integers(2, 3000, 2)
    N = 2*int(max(factorint(int(a*b))))+2
    sa,_ = signal(int(a), N); sb,_ = signal(int(b), N); sab,_ = signal(int(a*b), N)
    if np.max(np.abs(sa+sb-sab)) > 1e-9: bad += 1
res['mult_is_add_errors_2000'] = bad
# 3) Ic carpim: <s_a,s_b> = (N/2) sum v_p(a)v_p(b); ardisik sayilar dik
mx = 0
for n in range(2, 5001):
    N = 2*int(max(max(factorint(n)), max(factorint(n+1))))+2
    sa,_ = signal(n, N); sb,_ = signal(n+1, N)
    mx = max(mx, abs(sa@sb))
res['max_inner_n_n+1_2_5000'] = mx
# 4) Gurultu: s + N(0, sigma^2); tek dinleme, N ornek
noise = []
from scipy.stats import norm
NS = 2**15; nb = len(list(primerange(2, NS//2)))
for sigma in [4, 8, 12, 16, 20, 24, 32]:
    ok = 0; T = 300
    for _ in range(T):
        n = int(rng.integers(2, 10**4))       # P+(n) < 10^4 < NS/2: ortusme yok
        s, N = signal(n, NS)
        if decode(s + rng.normal(0, sigma, N)) == factorint(n): ok += 1
    # teori: her asal bininde genlik gurultusu sd = sigma*sqrt(2/N);
    # basari ~ P(z<0.5/sd)^(asal bin sayisi) (kod yalniz e>0 okur)
    sd = sigma*math.sqrt(2/NS)
    theory = (1-norm.sf(0.5/sd))**nb   # bos binlerde yalniz pozitif sapma hata
    noise.append((sigma, ok/T, round(theory,3)))
res['noise_N32768_(sigma,olculen,teori)'] = noise
# Bant siniri: N=4096 ornekle n<10^4: P+(n)>2047 olanlar katlanir (aliasing)
bad = sum(decode(signal(n,4096)[0]) != factorint(n) for n in range(2,10**4))
res['aliasing_N4096_n<1e4_errors'] = (bad, sum(max(factorint(n))>2047 for n in range(2,10**4)))
# 5) Maliyet: bant genisligi = en buyuk asal P+(n). Yari-asal n=p*q, p~q~sqrt n
cost = []
for d in [6, 10, 14, 18, 22, 26, 30]:
    p = randprime(10**(d//2-1), 10**(d//2)); q = randprime(10**(d//2-1), 10**(d//2))
    n = p*q
    t0 = time.perf_counter(); f = factorint(n); tf = time.perf_counter()-t0
    P = max(f)
    # FFT maliyeti ~ N log N, N=2P: dogrudan sadece kucuk P icin olc
    tfft = None
    if 2*P+2 < 2**23:
        s = np.zeros(2*P+2); t0=time.perf_counter(); np.fft.rfft(s); tfft=time.perf_counter()-t0
    cost.append(dict(digits=len(str(n)), factor_s=tf, P=int(P), samples=2*int(P)+2, fft_s=tfft))
res['cost_semiprimes'] = cost
# 6) Ortalama bant ussu log P+(n)/log n  (Golomb-Dickman sabiti 0.6243 e yakinsar)
M = 10**6
lpf = np.zeros(M+1, dtype=np.int64)
for p in primerange(2, M+1): lpf[p::p] = p   # buyuk asal en son yazilir
n = np.arange(2, M+1)
ratio = np.log(lpf[2:])/np.log(n)
res['mean_logP_over_logn_1e6'] = float(ratio.mean())
res['frac_P_gt_sqrt_n_1e6'] = float((lpf[2:]**2 > n).mean())   # teori: ln 2 = 0.693
# 7) n -> n+1 spektrum degisimi: ortak asal yok; spektral uzaklik
d = []
for n in range(2, 100001, 97):
    fa, fb = factorint(n), factorint(n+1)
    d.append(sum(v*v for v in fa.values()) + sum(v*v for v in fb.values()))
res['mean_lines_changed_n_to_n+1_(Sum v^2)'] = float(np.mean(d))
json.dump(res, open('/home/claude/civs/harmoni/sonuc_a.json','w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))

# WAV: 12, 360, 17 'nin sesi. Temel frekans f0=110 Hz: asal p -> p*f0 Hz
def wav(n, fn, f0=110, sr=8000, dur=0.8):
    t = np.arange(int(sr*dur))/sr
    s = sum(e*np.sin(2*np.pi*p*f0*t) for p, e in factorint(n).items())
    s = s/np.max(np.abs(s))*0.8*np.hanning(len(t))**0.2
    with wave.open(fn, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((s*32767).astype('<i2').tobytes())
for n in [12, 360, 17]: wav(n, f'/home/claude/civs/harmoni/ses_{n}.wav')
