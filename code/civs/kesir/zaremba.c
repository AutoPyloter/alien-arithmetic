/* Her q<=N icin:  Z(q)  = min_a max kismi bolum (a/q, gcd=1; son terim 1'e bolunebilir:
                           [..,a_n] = [..,a_n-1,1], bu yuzden a_n icin etkin deger a_n-1 de sayilir)
                   S(q)  = min_a  sum kismi bolumler  (Stern-Brocot derinligi + 1)
   a ve q-a ayni toplam/maks verir (ilk terim 1 eklenir/cikar) -> a <= q/2 yeter... (maks icin
   dikkat: q-a/q = [0;1,a1-1,...]; maks ayni ya da ayni). Guvenli olsun diye tum a<q taranir. */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char**argv){
  long N = atol(argv[1]);
  printf("q Z S\n");
  for(long q=2;q<=N;q++){
    int bestZ=1<<30; long bestS=1L<<60;
    for(long a=1;a<q;a++){
      long x=q,y=a; int mx=0; long s=0; int ok=1; long last=0;
      /* a/q = [0; a1, a2, ...]: x/y Euclid */
      while(y){ long t=x/y, r=x-t*y; s+=t; last=t; if(t>mx) mx=t; x=y; y=r; }
      if(x!=1) continue;            /* gcd != 1 */
      /* son terim indirimi: [..,t] = [..,t-1,1] */
      int mx2=0; { long X=q,Y=a; while(Y){ long t=X/Y,r=X-t*Y; if(r==0 && t>=2) t=t-1; if(t>mx2) mx2=t; X=Y; Y=r; } }
      /* mx2: son terim t-1 (t>=2 ise) ile maks; t-1 ve ek 1 -> maks(t-1,1) */
      int m = mx2<mx?mx2:mx;
      if(m<bestZ) bestZ=m;
      if(s<bestS) bestS=s;
    }
    printf("%ld %d %ld\n",q,bestZ,bestS);
  }
  return 0;
}
