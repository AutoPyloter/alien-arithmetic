/*
 * Descartes sayıları (tek sahte mükemmel sayılar) için kare taraması.
 *
 * Tanım (Tóth 2021): tek n, x ≥ 2 için σ(n)(x + 1) = 2 n x  ⇔  2n/σ(n) − 1 = 1/x.
 * D = n·x tek ise x tek; o zaman 2nx ≡ 2 (mod 4) ⇒ σ(n)(x+1) ≡ 2 (mod 4) ⇒ σ(n) tek.
 * n tek ve σ(n) tek ⇒ n tam kare. Dolayısıyla n = m² taramak yeterli:
 * n ≤ 10^12 taraması m ≤ 10^6 demek.
 *
 * Program [A, B) aralığındaki tek m'ler için σ(m²)'yi parçalı elekle hesaplar ve
 * d = 2m² − σ(m²) > 0 olup d | σ(m²) olan bütün m'leri (x = σ/d) yazdırır.
 * Kullanım: ./descartes_squares A B
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef unsigned __int128 u128;

static void print_u128(u128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    if (v == 0) { printf("0"); return; }
    while (v) { buf[--i] = '0' + (int)(v % 10); v /= 10; }
    printf("%s", buf + i);
}

int main(int argc, char **argv) {
    uint64_t A = strtoull(argv[1], 0, 10), B = strtoull(argv[2], 0, 10);
    uint64_t lim = (uint64_t)sqrtl((long double)B) + 2;
    /* küçük asallar */
    char *comp = calloc(lim + 1, 1);
    uint32_t *pr = malloc(sizeof(uint32_t) * (lim + 1)); size_t np = 0;
    for (uint64_t i = 2; i <= lim; i++) {
        if (!comp[i]) { pr[np++] = (uint32_t)i; for (uint64_t j = i * i; j <= lim; j += i) comp[j] = 1; }
    }
    const uint64_t SEG = 1 << 20;
    uint64_t *rem = malloc(sizeof(uint64_t) * SEG);
    u128 *val = malloc(sizeof(u128) * SEG);
    uint64_t found = 0;
    for (uint64_t lo = A; lo < B; lo += SEG) {
        uint64_t hi = lo + SEG < B ? lo + SEG : B, len = hi - lo;
        for (uint64_t i = 0; i < len; i++) { rem[i] = lo + i; val[i] = 1; }
        for (size_t k = 0; k < np; k++) {
            uint64_t p = pr[k];
            if (p * p >= hi) break;
            uint64_t st = (lo + p - 1) / p * p;
            for (uint64_t m = st; m < hi; m += p) {
                uint64_t i = m - lo;
                int a = 0;
                while (rem[i] % p == 0) { rem[i] /= p; a++; }
                /* σ(p^{2a}) = 1 + p + … + p^{2a} */
                u128 s = 1, pw = 1;
                for (int t = 0; t < 2 * a; t++) { pw *= p; s += pw; }
                val[i] *= s;
            }
        }
        for (uint64_t i = 0; i < len; i++) {
            uint64_t m = lo + i;
            if (m < 3 || (m & 1) == 0) continue;
            if (rem[i] > 1) { u128 r = rem[i]; val[i] *= (r * r + r + 1); }
            u128 n = (u128)m * m, s = val[i];
            if (s < 2 * n) {
                u128 d = 2 * n - s;
                if (s % d == 0) {
                    u128 x = s / d;
                    printf("m=%llu n=", (unsigned long long)m); print_u128(n);
                    printf(" x="); print_u128(x); printf("\n");
                    found++;
                }
            }
        }
    }
    fprintf(stderr, "done [%llu,%llu) found=%llu\n", (unsigned long long)A, (unsigned long long)B,
            (unsigned long long)found);
    return 0;
}
