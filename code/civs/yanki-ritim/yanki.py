"""Yankı uygarlığı: sayı = küçük asallara göre kalanlar vektörü (RNS)."""
import random, time, math
from sympy import primerange, isprime, primitive_root, factorint

BASE = [2, 3, 5, 7, 11, 13]          # yankı tabanı, M = 30030
M = math.prod(BASE)

def enc(n, base=BASE):  return tuple(n % p for p in base)
def add(x, y, base=BASE): return tuple((a + b) % p for a, b, p in zip(x, y, base))
def mul(x, y, base=BASE): return tuple((a * b) % p for a, b, p in zip(x, y, base))

def crt(x, base=BASE):
    """Çin kalan teoremi ile geri dönüş. İşlem sayısını da döndürür."""
    Mb = math.prod(base); s = 0; ops = 0
    for a, p in zip(x, base):
        Mi = Mb // p; s += a * Mi * pow(Mi, -1, p); ops += 3
    return s % Mb, ops

def mixed_radix(x, base=BASE):
    """Karışık taban dönüşümü: O(k^2) küçük işlem, büyük sayı yok."""
    a = list(x); digs = []; ops = 0
    for i, p in enumerate(base):
        d = a[i] % p; digs.append(d)
        for j in range(i + 1, len(base)):
            q = base[j]
            a[j] = ((a[j] - d) * pow(p, -1, q)) % q; ops += 2
    return digs, ops

def less_than(x, y, base=BASE):
    """Karşılaştırma: karışık taban hanelerini en anlamlıdan başlayarak kıyasla."""
    dx, _ = mixed_radix(x, base); dy, _ = mixed_radix(y, base)
    return dx[::-1] < dy[::-1]

def test_laws():
    random.seed(1); bad_add = bad_mul = bad_crt = bad_cmp = 0; N = 200000
    for _ in range(N):
        a, b = random.randrange(M), random.randrange(M)
        bad_add += enc((a + b) % M) != add(enc(a), enc(b))
        bad_mul += enc((a * b) % M) != mul(enc(a), enc(b))
        bad_crt += crt(enc(a))[0] != a
        bad_cmp += less_than(enc(a), enc(b)) != (a < b)
    print(f"Test: {N} rastgele çift, a,b < M={M}")
    print(f"  + hata {bad_add}, x hata {bad_mul}, CRT geri dönüş hata {bad_crt}, karşılaştırma hata {bad_cmp}")
    # karşılaştırma tek koordinata bakarak yapılamaz: her koordinat bilgisi diğerlerinden bağımsız
    # örnek: büyüklük bilgisinin tüm koordinatlara yayıldığını göster
    x, y = 29, 30
    print("  29 ->", enc(29), " 30 ->", enc(30), " 30029 ->", enc(30029))

def parity_of_sign_hint():
    """Hiçbir tek koordinat (veya k-1 koordinat) a<b sorusunu belirlemez: sayım."""
    # her (k-1) koordinat alt kümesi için, a<b'yi tahmin eden en iyi kural tüm bilgiyi kullanamaz
    sub = BASE[:-1]; Ms = math.prod(sub)
    # a ve b'nin ilk k-1 koordinatı sabitse, son koordinat 13 farklı yükseklik verir
    print(f"  ilk {len(sub)} koordinat sabit -> sayı {M//Ms} farklı değerden biri (aralık {Ms} adım):",
          [ (7 + Ms*j) for j in range(M//Ms)][:5], "...")

def cost_bench():
    random.seed(2)
    xs = [random.randrange(M) for _ in range(20000)]
    t = time.perf_counter(); E = [enc(a) for a in xs]; t_enc = time.perf_counter() - t
    t = time.perf_counter(); [crt(e) for e in E]; t_crt = time.perf_counter() - t
    t = time.perf_counter(); [mixed_radix(e) for e in E]; t_mr = time.perf_counter() - t
    t = time.perf_counter(); [add(E[i], E[i-1]) for i in range(len(E))]; t_add = time.perf_counter() - t
    t = time.perf_counter(); [mul(E[i], E[i-1]) for i in range(len(E))]; t_mul = time.perf_counter() - t
    k = len(BASE)
    print(f"Maliyet (20000 sayı, k={k} koordinat, saf Python, mikrosaniye/sayı):")
    print(f"  onluk->yankı {1e6*t_enc/2e4:.2f} | + {1e6*t_add/2e4:.2f} | x {1e6*t_mul/2e4:.2f} | "
          f"yankı->onluk CRT {1e6*t_crt/2e4:.2f} | karışık taban {1e6*t_mr/2e4:.2f}")
    print(f"  küçük işlem sayısı: enc {k}, +/x {k}, CRT {3*k} (büyük sayılarla), karışık taban {k*(k-1)} (küçük sayılarla)")

# ---------- harf -> yankı: indis tablosu ile doğrusal geçiş ----------
def letters(n):  # harf vektörü: {asal: üs}
    return factorint(n)

IND = {}
for p in BASE:
    if p == 2: continue
    g = primitive_root(p); t = {}
    x = 1
    for e in range(p - 1): t[x] = e; x = x * g % p
    IND[p] = (g, t)

def harf_to_yanki(v):
    """v: {asal: üs}. Her p için n mod p'yi doğrusal form L_p(v) ile bul. n'yi hiç kurmadan."""
    out = []; ops = 0
    for p in BASE:
        if v.get(p, 0) > 0: out.append(0); continue
        if p == 2: out.append(1); continue   # 2 harfi yoksa n tektir
        g, t = IND[p]; L = 0
        for q, e in v.items():
            L = (L + e * t[q % p]) % (p - 1); ops += 1
        out.append(pow(g, L, p))
    return tuple(out), ops

def test_harf_yanki():
    bad = 0; tot_ops = 0; N = 0; t_fac = 0
    for n in range(1, 200001):
        t = time.perf_counter(); v = letters(n); t_fac += time.perf_counter() - t
        y, ops = harf_to_yanki(v); tot_ops += ops; N += 1
        bad += y != enc(n)
    print(f"harf->yankı (indis tablosu, doğrusal form): n <= 200000, hata {bad}, ortalama {tot_ops/N:.2f} tablo işlemi")
    print(f"yankı->harf = çarpanlara ayırma; burada sympy factorint ortalama {1e6*t_fac/N:.1f} mikrosaniye (n<=2e5)")
    # yankı->harf'in imkânsızlığı: aynı yankı, farklı harfler
    y = enc(17); same = [n for n in range(17, 17 + 5 * M, M)]
    print("  aynı yankı", y, "taşıyan sayılar:", same, "harfleri:", [dict(letters(n)) for n in same])

# ---------- asallık: yankı ne söyler? ----------
def primality_view():
    # n < M için 'tüm koordinatlar sıfırdan farklı' = küçük asal bölen yok; asallık için yetmez
    surv = [n for n in range(14, M) if all(c != 0 for c in enc(n))]
    pr = [n for n in surv if isprime(n)]
    print(f"Asallık: 13 < n < {M}, tüm yankı koordinatları ≠ 0 olan {len(surv)} sayı, bunların {len(pr)} tanesi asal"
          f" (oran {len(pr)/len(surv):.3f}).")
    print(f"  n < M için kesin asallık testi, √M ≈ {int(M**0.5)}'e kadar {len(list(primerange(2, int(M**0.5)+1)))} asallık koordinat ister (taban {len(BASE)}).")

# ---------- Goldbach ve ikiz asallar: yerel 'yasak kalan' sayımı ----------
def local_counts():
    print("Goldbach: 2N = p + q. Her ℓ için p mod ℓ ∉ {0, 2N mod ℓ}: ℓ | 2N ise ℓ-1, değilse ℓ-2 izinli kalan.")
    import numpy as np
    X = 200000
    isp = np.ones(X + 1, bool); isp[:2] = False
    for p in range(2, int(X ** 0.5) + 1):
        if isp[p]: isp[p*p::p] = False
    P = np.nonzero(isp)[0]
    rows = []
    for N2 in range(100000, 100000 + 600, 2):
        q = N2 - P[(P >= 3) & (P <= N2 // 2)]
        reps = int(isp[q].sum())
        S = 1.0
        for l in primerange(3, N2 + 1):
            if l * l > N2 and N2 % l: 
                if l > 1000: break
            if N2 % l == 0: S *= (l - 1) / (l - 2)
        rows.append((N2, reps, S))
    import statistics
    for lo, hi in [(1.0, 1.01), (1.3, 1.4), (2.0, 2.1), (2.6, 2.8)]:
        sel = [r for _, r, S in rows if lo <= S < hi]
        if sel: print(f"  2N∈[100000,100600): yerel çarpan S∈[{lo},{hi}) -> {len(sel)} sayı, ortalama temsil {statistics.mean(sel):.0f}")
    rs = [r / S for _, r, S in rows]
    print(f"  temsil/S oranı: ortalama {statistics.mean(rs):.0f}, göreli sapma {statistics.pstdev(rs)/statistics.mean(rs):.3f}"
          f" (ham temsilin göreli sapması {statistics.pstdev([r for _,r,_ in rows])/statistics.mean([r for _,r,_ in rows]):.3f})")
    print("İkiz asallar (p, p+2): her ℓ ≥ 3 için p mod ℓ ∉ {0, ℓ-2}: izinli ℓ-2 kalan.")

def sieve_vs_truth(X=10**6):
    """Yankı eleği: küçük asallarda yerel kaçınma, kalanlar ile gerçek ikiz asal sayısı."""
    import numpy as np
    n = np.arange(X + 3)
    isp = np.ones(X + 3, bool); isp[:2] = False
    for p in range(2, int((X + 3) ** 0.5) + 1):
        if isp[p]: isp[p*p::p] = False
    twins = int(np.sum(isp[3:X] & isp[5:X+2]))
    print(f"İkiz asal çifti sayısı p < {X}: {twins}")
    for z in [3, 5, 7, 13, 31, 100, 1000]:
        ok = np.ones(X, bool); ok[:3] = False
        for l in primerange(3, z + 1):
            r = n[:X] % l
            ok &= (r != 0) & (r != l - 2)
        ok &= (n[:X] % 2 == 1)
        # kalanlar (z'den küçük gerçek ikizler dışarıda kalır)
        print(f"  z={z:5d}: yerel koşulları sağlayan p<X sayısı {int(ok.sum()):7d}, bunlardan ikiz {int((ok & isp[:X] & isp[2:X+2]).sum())}")

def parity_barrier(X=10**6):
    """Parite duvarı: elekten geçenlerde λ(n)=+1 ve -1 olanlar yerel koşullarla ayırt edilemez."""
    import numpy as np
    z = int(round(X ** (1/3)))
    spf = np.zeros(X + 1, np.int64)
    for p in primerange(2, X + 1):
        if p * p > X: break
    # Ω(n) hesapla
    Omega = np.zeros(X + 1, np.int64); rem = np.arange(X + 1)
    for p in primerange(2, int(X**0.5) + 1):
        pk = p
        while pk <= X:
            Omega[pk::pk] += 1; rem[pk::pk] //= p; pk *= p
    Omega += (rem > 1)
    n = np.arange(X + 1); ok = n > z
    for p in primerange(2, z + 1): ok &= (n % p != 0)
    cnt1 = int(np.sum(ok & (Omega == 1))); cnt2 = int(np.sum(ok & (Omega == 2)))
    print(f"Parite: n ≤ {X}, p ≤ z={z} için tüm yankı koordinatları ≠ 0 olan {int(ok.sum())} sayı:")
    print(f"  Ω=1 (asal, λ=-1): {cnt1},  Ω=2 (iki büyük harf, λ=+1): {cnt2}")
    # her küçük modülde iki sınıf aynı dağılır mı?
    for l in [3, 5, 7, 11]:
        a = np.bincount(n[ok & (Omega == 1)] % l, minlength=l)[1:] / cnt1
        b = np.bincount(n[ok & (Omega == 2)] % l, minlength=l)[1:] / cnt2
        print(f"  mod {l}: asallar {np.round(a,3)} | iki-harfliler {np.round(b,3)}")

if __name__ == "__main__":
    test_laws(); parity_of_sign_hint(); cost_bench(); test_harf_yanki(); primality_view()
    local_counts(); sieve_vs_truth(); parity_barrier()
