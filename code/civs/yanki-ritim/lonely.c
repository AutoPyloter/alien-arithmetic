/* Yalnız koşucu: k koşucu, tamsayı hızlar 0 = w_0 < w_1 < ... < w_{k-1} <= VMAX (öteleme
   değişmezliği yüzünden en yavaşı 0 alınabilir). Her koşucu i için
   delta_i = max_t min_{j!=i} ||t (w_j - w_i)||  tam (rasyonel) olarak hesaplanır.
   Aday zamanlar t = m/(d_a + d_b) (a=b dahil): parçalı doğrusal fonksiyonun tepe noktaları.
   Sanı: her i için delta_i >= 1/k. Çıktı: en kötü (k*delta en küçük) durumlar ve sıkı durumların sayısı. */
#include <stdio.h>
#include <stdlib.h>
static int K, VMAX;
static long long nsets = 0, ntight = 0, nfail = 0;
static double worst = 1e9; static int worstw[16], worsti; static long long wn, wd, wm, wD;
static int w[16]; static long long nprim_tight=0; static double worst2=1e9; static int w2[16], w2i; static long long w2n,w2d,w2m,w2D;
static int gcd(int a,int b){while(b){int t=a%b;a=b;b=t;}return a;}
/* runner i için delta = bn/bd, zaman bm/bD */
static void runner(int i, long long *bn, long long *bd, long long *bm, long long *bD){
  int d[16], n = 0;
  for (int j = 0; j < K; j++) if (j != i) { int x = abs(w[j] - w[i]); int dup = 0;
      for (int t = 0; t < n; t++) if (d[t] == x) dup = 1; if (!dup) d[n++] = x; }
  long long BN = 0, BD = 1, BM = 0, BDD = 1;
  for (int a = 0; a < n; a++) for (int b = a; b < n; b++) {
    long long D = d[a] + d[b];
    for (long long m = 1; m < D; m++) {
      long long mn = D;
      for (int t = 0; t < n; t++) { long long r = (m * d[t]) % D; if (D - r < r) r = D - r; if (r < mn) mn = r; if (mn * BD <= BN * D) break; }
      if (mn * BD > BN * D) { BN = mn; BD = D; BM = m; BDD = D; }
    }
  }
  *bn = BN; *bd = BD; *bm = BM; *bD = BDD;
}
static void rec(int pos, int lo){
  if (pos == K) {
    /* gcd'si 1 olmayanlar ölçeklenmiş kopya; yine de say */
    nsets++; int tight = 0, fail = 0;
    for (int i = 0; i < K; i++) {
      long long bn, bd, bm, bD; runner(i, &bn, &bd, &bm, &bD);
      double r = (double)K * bn / bd;
      if (bn * K < bd) fail = 1;
      if (bn * K == bd) tight = 1;
      if (bn * K > bd && r < worst2 - 1e-12) { worst2 = r; for (int t = 0; t < K; t++) w2[t] = w[t]; w2i = i; w2n = bn; w2d = bd; w2m = bm; w2D = bD; }
      if (r < worst - 1e-12) { worst = r; for (int t = 0; t < K; t++) worstw[t] = w[t]; worsti = i; wn = bn; wd = bd; wm = bm; wD = bD; }
    }
    ntight += tight; nfail += fail;
    int g = 0; for (int t = 1; t < K; t++) g = gcd(g, w[t]);
    if (tight && g == 1) nprim_tight++;
    if (tight && g == 1 && w[K-1] <= 30 && getenv("LIST")) { printf("  sıkı: {"); for (int t = 0; t < K; t++) printf("%d%s", w[t], t < K-1 ? "," : ""); printf("}\n"); }
    return;
  }
  for (int v = lo; v <= VMAX; v++) { w[pos] = v; rec(pos + 1, v + 1); }
}
int main(int argc, char **argv){
  K = atoi(argv[1]); VMAX = atoi(argv[2]); w[0] = 0; rec(1, 1);
  printf("K=%d koşucu, hızlar 0..%d: %lld küme, sanıyı bozan %lld, sıkı (bir koşucu tam 1/K) %lld\n", K, VMAX, nsets, nfail, ntight);
  printf("  en kötü: hızlar {"); for (int t = 0; t < K; t++) printf("%d%s", worstw[t], t < K-1 ? "," : "");
  printf("}, koşucu hızı %d, en iyi uzaklık %lld/%lld (K*delta = %.6f), zaman t = %lld/%lld\n", worstw[worsti], wn, wd, worst, wm, wD);
  printf("  ilkel (ebob=1) sıkı küme: %lld\n", nprim_tight);
  printf("  sıkı olmayanların en kötüsü: {"); for (int t = 0; t < K; t++) printf("%d%s", w2[t], t < K-1 ? "," : "");
  printf("}, koşucu hızı %d, uzaklık %lld/%lld (K*delta = %.6f), t = %lld/%lld\n", w2[w2i], w2n, w2d, worst2, w2m, w2D);
  return 0;
}
