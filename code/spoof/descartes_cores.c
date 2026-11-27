/*
 * Descartes sayıları için çekirdek taraması (descartes_squares.c'nin hızlı sürümü).
 *
 * Teorem 3: x ≥ 5 (x tek, x ≡ 1 mod 4) ⇒ σ(m²)/m² = 2 − 1/k ≥ 5/3.
 * Teorem 4: σ(m²)/m² < ∏_{p | m} p/(p−1) ⇒ ∏_{p | m} p/(p−1) > 5/3.
 *
 * m'nin asallarını artan sırada dizince, p/(p−1) çarpımının ilk kez 5/3'ü aştığı önek
 * C = {p_1 < … < p_j} "çekirdek" olsun ve c = p_1⋯p_j. O zaman m = c·t; t'nin her asal
 * böleni ya C'de ya da p_j'den büyük. Her m en fazla bir çekirdeğe düşer. Çekirdeği
 * olmayan m'ler Teorem 4'e göre Descartes sayısı veremez. (Eşik, tek büyük asal payıyla
 * (5/3)(Q−1)/Q'ya indirilir; böylece çekirdeğin bütün asalları Q = max(√B, 2·10⁶) altında kalır.)
 *
 * Kullanım: ./descartes_cores A B   (A ≤ m < B, tek m)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

typedef unsigned __int128 u128;
static uint32_t *pr; static size_t np;
static uint64_t A, B;
static uint64_t found = 0, cores = 0;
static long double work = 0;
static long double TH;   /* (5/3)·(Q−1)/Q: m'nin Q'dan büyük en fazla bir asalı olabilir */

static void print_u128(u128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    if (v == 0) { printf("0"); return; }
    while (v) { buf[--i] = '0' + (int)(v % 10); v /= 10; }
    printf("%s", buf + i);
}

#define SEG (1u << 18)
static uint64_t rem_[SEG]; static u128 val_[SEG]; static uint16_t seen_[SEG]; static uint8_t bad_[SEG];

/* çekirdek c (asallar C[0..k-1], hepsi tek) için tek t'leri tara: A ≤ c·t < B */
static void scan_core(uint64_t c, const uint32_t *C, int k) {
    uint32_t P = C[k - 1];
    uint64_t t0 = (A + c - 1) / c, t1 = (B + c - 1) / c;   /* t ∈ [t0, t1) */
    if (t0 < 1) t0 = 1;
    if ((t0 & 1) == 0) t0++;
    if (t0 >= t1) return;
    cores++; work += (long double)(t1 - t0) / 2;
    uint64_t lim = (uint64_t)sqrtl((long double)t1) + 1;
    for (uint64_t lo = t0; lo < t1; lo += 2 * (uint64_t)SEG) {
        uint64_t hi = lo + 2 * (uint64_t)SEG < t1 ? lo + 2 * (uint64_t)SEG : t1;
        uint64_t len = (hi - lo + 1) / 2;
        for (uint64_t i = 0; i < len; i++) { rem_[i] = lo + 2 * i; val_[i] = 1; seen_[i] = 0; bad_[i] = 0; }
        for (size_t j = 1; j < np; j++) {
            uint64_t p = pr[j];
            if (p > lim) break;
            int ci = -1;
            for (int q = 0; q < k; q++) if (C[q] == p) { ci = q; break; }
            int forbid = (ci < 0 && p < P);            /* çekirdek dışı küçük asal yasak */
            uint64_t st = (lo + p - 1) / p * p;
            if ((st & 1) == 0) st += p;
            for (uint64_t t = st; t < hi; t += 2 * p) {
                uint64_t i = (t - lo) >> 1;
                if (bad_[i]) continue;
                if (forbid) { bad_[i] = 1; continue; }
                int a = 0;
                while (rem_[i] % p == 0) { rem_[i] /= p; a++; }
                int e = a + (ci >= 0 ? 1 : 0);          /* m'deki üs */
                u128 s = 1, pw = 1;
                for (int z = 0; z < 2 * e; z++) { pw *= p; s += pw; }
                val_[i] *= s;
                if (ci >= 0) seen_[i] |= (uint16_t)(1u << ci);
            }
        }
        for (uint64_t i = 0; i < len; i++) {
            if (bad_[i]) continue;
            u128 v = val_[i];
            if (rem_[i] > 1) {
                u128 r = rem_[i];
                /* kalan büyük asal: çekirdekte mi, yasak mı? */
                int ci = -1;
                for (int q = 0; q < k; q++) if (C[q] == rem_[i]) { ci = q; break; }
                if (ci >= 0) { u128 s = 1, pw = 1; for (int z = 0; z < 4; z++) { pw *= r; s += pw; } v *= s; seen_[i] |= (uint16_t)(1u << ci); }
                else if (rem_[i] < P) continue;
                else v *= (r * r + r + 1);
            }
            for (int q = 0; q < k; q++) if (!(seen_[i] & (1u << q))) { u128 p = C[q]; v *= (p * p + p + 1); }
            uint64_t t = lo + 2 * i;
            u128 m = (u128)c * t;
            u128 n = m * m, s = v;
            if (s < 2 * n) {
                u128 d = 2 * n - s;
                if (s % d == 0 && n % d == 0) {
                    printf("m="); print_u128(m); printf(" n="); print_u128(n);
                    printf(" x="); print_u128(s / d); printf(" core=%llu\n", (unsigned long long)c);
                    found++;
                }
            }
        }
    }
}

static uint32_t Cbuf[32];
static void dfs(uint64_t c, long double r, size_t j0, int k) {
    for (size_t j = j0; j < np; j++) {
        uint64_t q = pr[j];
        if ((u128)c * q >= B) break;
        long double r2 = r * (long double)q / (long double)(q - 1);
        Cbuf[k] = (uint32_t)q;
        if (r2 > TH) { scan_core(c * q, Cbuf, k + 1); continue; }
        /* kalan en fazla w asal (hepsi ≥ q): c·q^w < B */
        int w = 0; u128 cc = c;
        while (cc * q < B) { cc *= q; w++; }
        long double best = r; for (int z = 0; z < w; z++) best *= (long double)q / (long double)(q - 1);
        if (best <= TH) break;
        dfs(c * q, r2, j + 1, k + 1);
    }
}

int main(int argc, char **argv) {
    A = strtoull(argv[1], 0, 10); B = strtoull(argv[2], 0, 10);
    /* asallar: çekirdek ve elek için √B'ye kadar + çekirdek asalları için daha büyükleri gerekebilir */
    uint64_t lim = (uint64_t)sqrtl((long double)B) + 2;
    if (lim < 2000000) lim = 2000000;
    char *comp = calloc(lim + 1, 1);
    pr = malloc(sizeof(uint32_t) * (lim + 1)); np = 0;
    for (uint64_t i = 2; i <= lim; i++) {
        if (!comp[i]) { pr[np++] = (uint32_t)i; for (uint64_t j = i * i; j <= lim; j += i) comp[j] = 1; }
    }
    /* Q = lim ≥ √B: m < B'nin Q'dan büyük en fazla bir asal böleni var ve onun katkısı < Q/(Q−1).
       Dolayısıyla m'nin Q'ya kadar olan asallarının çarpımı > (5/3)(Q−1)/Q olmalı. */
    TH = (5.0L / 3.0L) * (long double)(lim - 1) / (long double)lim - 1e-12L;
    dfs(1, 1.0L, 1, 0);   /* pr[0] = 2 atlanır */
    fprintf(stderr, "done [%llu,%llu) cores=%llu found=%llu scanned_t=%.3Le\n",
            (unsigned long long)A, (unsigned long long)B, (unsigned long long)cores,
            (unsigned long long)found, work);
    return 0;
}
