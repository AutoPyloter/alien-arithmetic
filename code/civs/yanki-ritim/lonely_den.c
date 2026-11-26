/* Duran koşucu, n hız 1 <= v_1 < ... < v_n <= VMAX, ebob = 1.
   D*(v) = en küçük D: bir m için her i, (n+1) * dist(m v_i mod D, 0) >= D  (t = m/D anında yalnız).
   Ayrıca D* asal mı? İstatistik: max D*, D* dağılımı, D*'ın asal / n+1 olma oranı. */
#include <stdio.h>
#include <stdlib.h>
static int N, VMAX, v[16];
static long long cnt = 0, hist[4096], prime_cnt = 0, eq_n1 = 0; static int maxD = 0, maxv[16];
static int gcd(int a, int b){ while (b){ int t = a % b; a = b; b = t; } return a; }
static int isprime(int x){ if (x < 2) return 0; for (int d = 2; d * d <= x; d++) if (x % d == 0) return 0; return 1; }
static int dstar(void){
  for (int D = 2; D < 4096; D++)
    for (int m = 1; m < D; m++) { int ok = 1;
      for (int i = 0; i < N; i++) { int r = (int)(((long long)m * v[i]) % D); if (D - r < r) r = D - r; if ((N + 1) * r < D) { ok = 0; break; } }
      if (ok) return D; }
  return -1;
}
static void rec(int pos, int lo){
  if (pos == N) { int g = 0; for (int i = 0; i < N; i++) g = gcd(g, v[i]); if (g != 1) return;
    int D = dstar(); cnt++; hist[D]++; prime_cnt += isprime(D); eq_n1 += (D == N + 1);
    if (D > maxD) { maxD = D; for (int i = 0; i < N; i++) maxv[i] = v[i]; } return; }
  for (int x = lo; x <= VMAX; x++) { v[pos] = x; rec(pos + 1, x + 1); }
}
int main(int c, char **a){ N = atoi(a[1]); VMAX = atoi(a[2]); rec(0, 1);
  printf("n=%d hız (duran koşucu), hızlar <= %d, ebob=1: %lld küme | max D* = %d hızlar {", N, VMAX, cnt, maxD);
  for (int i = 0; i < N; i++) printf("%d%s", maxv[i], i < N-1 ? "," : "}");
  printf(" | D* asal: %.3f | D* = n+1: %.3f\n  D* dağılımı:", (double)prime_cnt / cnt, (double)eq_n1 / cnt);
  for (int D = 0; D < 4096; D++) if (hist[D]) printf(" %d:%lld", D, hist[D]); printf("\n"); return 0; }
