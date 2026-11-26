/* Pencere W_k = (F_k, F_{k+1}] icindeki her q icin S(q) = min kismi bolum toplami.
   s_min(q) = k. E(q) = S(q) - k. Toplami <= k+C olan tum kompozisyonlar DFS ile, budamali.
   Kullanim: ./window k C   -> E dagilimi ve kapsanmayan (E > C) sayisi */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
u64 F[100]; int k, C, budget; u64 lo, hi; unsigned char *best; u64 nodes = 0;
void dfs(u64 kp, u64 kc, int s){
  nodes++;
  if (kc > lo && kc <= hi){ int e = s - k; unsigned char *b = &best[kc - lo - 1]; if (e < *b) *b = e; }
  int r = budget - s;
  for (int a = 1; a <= r; a++){
    u64 kn = a * kc + kp;
    if (kn > hi) break;
    int r2 = r - a;
    /* kalan r2 birle ulasilabilecek en buyuk: kn*F[r2+1] + kc*F[r2] */
    if (kn * F[r2+1] + kc * F[r2] <= lo) continue;   /* a buyudukce artar, devam */
    dfs(kc, kn, s + a);
  }
}
int main(int argc, char **argv){
  k = atoi(argv[1]); C = atoi(argv[2]); budget = k + C;
  F[0]=0; F[1]=1; for(int i=2;i<100;i++) F[i]=F[i-1]+F[i-2];
  lo = F[k]; hi = F[k+1]; u64 W = hi - lo;
  best = malloc(W); memset(best, 255, W);
  dfs(0, 1, 0);
  u64 cnt[20] = {0}, unc = 0; long double sum = 0;
  for (u64 i = 0; i < W; i++){ if (best[i] == 255) unc++; else { cnt[best[i]]++; sum += best[i]; } }
  printf("k=%d F_k=%llu F_k+1=%llu W=%llu dugum=%llu  ", k, lo, hi, W, nodes);
  for (int e = 0; e <= C; e++) printf("E%d=%llu ", e, cnt[e]);
  printf("kapsanmayan(E>%d)=%llu  ort(E|<=C)=%.4Lf\n", C, unc, sum / (W - unc));
  if (unc && unc < 20){ printf("  E>%d olan q:", C); for (u64 i=0;i<W;i++) if(best[i]==255) printf(" %llu", lo+1+i); printf("\n"); }
  return 0;
}
