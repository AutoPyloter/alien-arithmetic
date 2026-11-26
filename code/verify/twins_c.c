/*
 * twins_c.c — σ-ikizlerinin bağımsız taraması (Alien Arithmetic, Katman 2)
 * Independent search for shift twins sigma(n+1) = sigma(n) + 2, 1 <= n <= N.
 *
 * sigma = OEIS A003961 (her asal çarpanı sonraki asalla değiştir).
 *
 * Yöntem (orijinal Numba/float-log taramasından BAĞIMSIZ):
 *   - Segmentli elek: p <= sqrt(N+1) asalları için n'nin p-kısmı tam sayı olarak
 *     ayrılır, S(n) = sigma(p-düzgün kısım) TAM olarak hesaplanır (uint64; N <= 1e11
 *     için sigma(n) < 2^64).
 *   - Kalan kofaktör q ya 1'dir ya da tek bir asal (q > sqrt(N+1)).
 *   - q > 1 ise sigma(n) = S(n) * nextprime(q) ve nextprime(q) ∈ [q+1, q+G].
 *     Böylece sigma(n) için TAM SAYI aralığı elde edilir (kayan nokta yok).
 *   - n aday sayılır ancak ve ancak [lo(n)+2, hi(n)+2] ile [lo(n+1), hi(n+1)] kesişirse.
 *   - Her aday, Miller–Rabin (64-bit için deterministik tabanlar) ile tam hesaplanır.
 *
 * G varsayımı: q < 1e11 için asal boşluk <= 464 (Nicely'nin maksimal boşluk tabloları;
 * 464 boşluğu 42652618343'te, sonraki rekor 468, 127976334671'de). Güvenlik payı
 * olarak G = 1000 kullanılır. G yalnızca filtreyi etkiler; aday doğrulaması tamdır.
 *
 * Derleme: gcc -O3 -march=native -fopenmp twins_c.c -o twins_c -lm
 * Kullanım: ./twins_c N [segment_size]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#ifdef _OPENMP
#include <omp.h>
#endif

typedef unsigned __int128 u128;
#define GAP 1000ULL

static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m) { return (u128)a * b % m; }
static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1; a %= m;
    while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; }
    return r;
}
/* 64-bit için deterministik Miller–Rabin */
static int is_prime_u64(uint64_t n) {
    if (n < 2) return 0;
    static const uint64_t sp[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (int i = 0; i < 12; i++) { if (n % sp[i] == 0) return n == sp[i]; }
    uint64_t d = n - 1; int s = 0;
    while ((d & 1) == 0) { d >>= 1; s++; }
    for (int i = 0; i < 12; i++) {
        uint64_t x = powmod(sp[i], d, n);
        if (x == 1 || x == n - 1) continue;
        int ok = 0;
        for (int r = 1; r < s; r++) { x = mulmod(x, x, n); if (x == n - 1) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}
static uint64_t next_prime_u64(uint64_t p) { uint64_t q = p + 1; while (!is_prime_u64(q)) q++; return q; }

/* Tam sigma (deneme bölmesi + MR) — yalnızca adaylar için */
static uint64_t sigma_exact(uint64_t n) {
    uint64_t r = 1;
    for (uint64_t p = 2; p * p <= n; p += (p == 2 ? 1 : 2)) {
        if (n % p == 0) { uint64_t np = next_prime_u64(p); while (n % p == 0) { n /= p; r *= np; } }
    }
    if (n > 1) r *= next_prime_u64(n);
    return r;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s N [seg]\n", argv[0]); return 1; }
    uint64_t N = strtoull(argv[1], 0, 10);
    uint64_t SEG = argc > 2 ? strtoull(argv[2], 0, 10) : (1ULL << 22);
    uint64_t lim = (uint64_t)sqrtl((long double)(N + 2)) + 2;
    /* küçük asallar ve sonrakileri */
    uint64_t plim = lim + 2000;
    char *comp = calloc(plim + 1, 1);
    uint64_t *pr = malloc(sizeof(uint64_t) * (plim / 2 + 10)); size_t np_ = 0;
    for (uint64_t i = 2; i <= plim; i++) {
        if (!comp[i]) { pr[np_++] = i; for (uint64_t j = i * i; j <= plim; j += i) comp[j] = 1; }
    }
    size_t nsmall = 0; while (nsmall < np_ && pr[nsmall] <= lim) nsmall++;
    uint64_t *nxt = malloc(sizeof(uint64_t) * nsmall);
    for (size_t i = 0; i < nsmall; i++) nxt[i] = pr[i + 1];

    uint64_t nseg = (N + SEG - 1) / SEG;
    uint64_t total_cand = 0, total_twins = 0;
    uint64_t *found = malloc(sizeof(uint64_t) * 100000); size_t nfound = 0;

    #pragma omp parallel for schedule(dynamic,1) reduction(+:total_cand,total_twins)
    for (uint64_t s = 0; s < nseg; s++) {
        uint64_t lo = 1 + s * SEG;                 /* n aralığı [lo, hi] */
        uint64_t hi = lo + SEG - 1; if (hi > N) hi = N;
        uint64_t len = hi - lo + 2;                /* n+1 için bir fazla */
        uint64_t *rem = malloc(8 * len), *sm = malloc(8 * len);
        for (uint64_t i = 0; i < len; i++) { rem[i] = lo + i; sm[i] = 1; }
        for (size_t k = 0; k < nsmall; k++) {
            uint64_t p = pr[k], q = nxt[k];
            uint64_t st = (p - lo % p) % p;
            for (uint64_t i = st; i < len; i += p) {
                do { rem[i] /= p; sm[i] *= q; } while (rem[i] % p == 0);
            }
        }
        for (uint64_t i = 0; i + 1 < len; i++) {
            uint64_t a_lo, a_hi, b_lo, b_hi;
            if (rem[i] == 1) { a_lo = a_hi = sm[i]; }
            else { a_lo = sm[i] * (rem[i] + 1); a_hi = sm[i] * (rem[i] + GAP); }
            if (rem[i+1] == 1) { b_lo = b_hi = sm[i+1]; }
            else { b_lo = sm[i+1] * (rem[i+1] + 1); b_hi = sm[i+1] * (rem[i+1] + GAP); }
            /* sigma(n+1) = sigma(n) + 2 mümkün mü? */
            if (b_lo <= a_hi + 2 && b_hi >= a_lo + 2) {
                total_cand++;
                uint64_t n = lo + i;
                uint64_t x = (rem[i] == 1) ? sm[i] : sm[i] * next_prime_u64(rem[i]);
                uint64_t y = (rem[i+1] == 1) ? sm[i+1] : sm[i+1] * next_prime_u64(rem[i+1]);
                if (y == x + 2) {
                    /* bağımsız ikinci kontrol: deneme bölmesiyle tam sigma */
                    if (sigma_exact(n + 1) != sigma_exact(n) + 2) {
                        fprintf(stderr, "TUTARSIZLIK n=%llu\n", (unsigned long long)n); exit(2);
                    }
                    total_twins++;
                    #pragma omp critical
                    { found[nfound++] = n; }
                }
            }
        }
        free(rem); free(sm);
    }
    /* sırala ve yaz */
    for (size_t i = 1; i < nfound; i++) { uint64_t v = found[i]; size_t j = i;
        while (j > 0 && found[j-1] > v) { found[j] = found[j-1]; j--; } found[j] = v; }
    printf("N=%llu adaylar=%llu ikizler=%llu\n", (unsigned long long)N,
           (unsigned long long)total_cand, (unsigned long long)total_twins);
    for (size_t i = 0; i < nfound; i++) printf("%llu\n", (unsigned long long)found[i]);
    return 0;
}
