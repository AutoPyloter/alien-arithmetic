"""Uygarligin 'asallari': Fermat asallari ve Gauss-Wantzel.

1) Pepin testi: F_n asal <=> 3^((F_n-1)/2) = -1 (mod F_n), n >= 1.
2) Bilinen kucuk carpanlarin dogrulanmasi.
3) Fermat asallari icin bagimsizlik sezgiseli (beklenen sayi).
4) Kuzen (origami) uygarliginin asallari: Pierpont asallari 2^u 3^v + 1, sayim vs sezgisel.
"""
import math, time, sys
import sympy as sp


def F(n):
    return (1 << (1 << n)) + 1


def pepin(n):
    N = F(n)
    return pow(3, (N - 1) // 2, N) == N - 1


def main(maxn=15):
    print("== Pepin testi ==")
    for n in range(0, maxn + 1):
        t = time.time()
        if n == 0:
            r = True
        else:
            r = pepin(n)
        print(f"  F{n}: {'ASAL' if r else 'bilesik'}  ({len(str(F(n))) if n < 14 else int((1 << n) * math.log10(2)) + 1} basamak, {time.time()-t:.1f}s)")
    print("\n== Bilinen carpanlar (k*2^m+1 | F_n kontrolu: 2^(2^n) = -1 mod p) ==")
    known = [(5, 641), (5, 6700417), (6, 274177), (6, 67280421310721), (7, 59649589127497217),
             (8, 1238926361552897), (9, 2424833), (10, 45592577), (11, 319489), (11, 974849),
             (12, 7 * 2 ** 14 + 1), (12, 397 * 2 ** 16 + 1), (12, 973 * 2 ** 16 + 1),
             (13, 2710954639361), (15, 579 * 2 ** 21 + 1), (16, 1575 * 2 ** 19 + 1), (18, 13 * 2 ** 20 + 1),
             (19, 33629 * 2 ** 21 + 1), (23, 5 * 2 ** 25 + 1), (36, 5 * 2 ** 39 + 1), (38, 3 * 2 ** 41 + 1)]
    for n, p in known:
        ok = pow(2, 1 << n, p) == p - 1
        print(f"  {p} | F{n}: {ok}; p asal: {sp.isprime(p)}")
    print("  F5 = 641 * 6700417:", F(5) == 641 * 6700417)
    print("  Ikili aralarinda asallik (Goldbach): gcd(F_i,F_j)=1, i<j<=12:",
          all(math.gcd(F(i), F(j)) == 1 for i in range(13) for j in range(i + 1, 13)))
    print("  F_n = F_0 F_1 ... F_{n-1} + 2 (n<=12):",
          all(math.prod(F(i) for i in range(n)) + 2 == F(n) for n in range(1, 13)))

    print("\n== Sezgisel: kac Fermat asali beklenir? ==")
    # Her asal bolen p | F_n, p = 1 mod 2^(n+2) (Lucas). Kaba model: P(F_n asal) ~ 2/ln F_n
    # (tekligi icin 2 carpani). Bilinen bilesikler (5..32) disinda kalan beklenti:
    tail = sum(2 * 2.0 ** (-n) / math.log(2) for n in range(33, 2000))
    allx = sum(2 * 2.0 ** (-n) / math.log(2) for n in range(0, 2000))
    print(f"  model, n>=0 toplami: {allx:.4f} ; n>=33 icin beklenen asal sayisi: {tail:.3e}")

    print("\n== Origami uygarligi: Pierpont asallari 2^u 3^v + 1 ==")
    for k in (10, 20, 40, 60, 80, 100):
        N = 10 ** k
        cnt = 0
        u = 0
        while (1 << u) <= N:
            v = 0
            while (1 << u) * 3 ** v + 1 <= N:
                if sp.isprime((1 << u) * 3 ** v + 1):
                    cnt += 1
                v += 1
            u += 1
        print(f"  <= 10^{k}: {cnt} Pierpont asali")
    from math import comb, prod
    from itertools import combinations
    Fp = [3, 5, 17, 257, 65537]
    odd = sorted(prod(c) for r in range(6) for c in combinations(Fp, r))
    rows = sorted(int("".join(str(comb(n, k) % 2) for k in range(n + 1)), 2) for n in range(32))
    print(f"\n  Tek cizilebilir n (bilinen Fermat asallarinin farkli carpimlari): {len(odd)} tane (1 dahil); "
          f"Pascal ucgeni mod 2'nin ilk 32 satiri (ikili okunur) ile ayni: {odd == rows}; en buyuk = 2^32-1: {odd[-1] == 2**32 - 1}")
    fp = sum(1 for n in range(0, 34) if n <= 4)
    print(f"  karsilastirma: Fermat asallari (bilinen) = {fp}, hepsi <= 65537")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
