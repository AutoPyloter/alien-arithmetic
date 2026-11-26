# σ-ikizi tamlık doğrulaması

İki güvence ayrı ayrı kuruluyor:

1. **Doğruluk:** Bulunan her n gerçekten σ(n+1) = σ(n) + 2 sağlıyor mu?
2. **Tamlık:** Aralıkta başka ikiz kalmadığından emin miyiz?

| Katman | Aralık | Güvence | Dosya |
|---|---|---|---|
| 1 | 1 ≤ n ≤ 10⁶ | Doğruluğu Lean'de ispatlı algoritma + `native_decide` | `lean/FastSigma.lean`, `lean/TwinCertificate.lean` |
| 2 | 1 ≤ n ≤ 10¹¹ | Bağımsız ikinci uygulama (C, tam sayı aralıkları) | `twins_c.c` |
| — | 1 ≤ n ≤ 10¹¹ | Orijinal tarama (Numba, kayan nokta log filtresi + mod-asal kontrol) | Colab (bkz. `notes/uzayli_defteri.md`) |

## Katman 1 — Lean

- **`FastSigma.lean`**: Hızlı bir σ hesaplayıcısı tanımlanıyor ve gerçek σ'ya eşit olduğu **koşulsuz** ispatlanıyor (`sigmaFast_eq`). Kullanılan yapı taşları:
  - Kareköke kadar asallık testi (`isPrimeFast_iff`).
  - Kareköke kadar en küçük bölen (`minFacFast_eq`).
  - Sınırlı arama yapan sonraki asal (`nextFast_eq`). Arama bir asal bulamazsa güvenli yavaş tanıma geri dönüyor; bu yüzden eşitlik her durumda geçerli.
- **Tarama döngüsü** `twinScan` için üyelik karakterizasyonu ispatlı (`twinScan_mem`).
- **`twins_certificate`**: Hesaplanan liste L ise, gerçek σ için "σ(n+1) = σ(n) + 2 ⇔ n ∈ L" (1 ≤ n ≤ N).
- **`TwinCertificate.lean`**: N = 10⁶ için listeyi `native_decide` ile hesaplayıp `twins_complete_1e6` teoremini üretiyor.

Güven tabanı: Lean çekirdeği + Lean derleyicisi (`Lean.ofReduceBool`). Algoritmanın doğruluğu kernel tarafından denetleniyor; yalnızca hesaplamanın kendisi derlenmiş kodla yapılıyor.

## Katman 2 — Bağımsız C tarayıcısı (`twins_c.c`)

Orijinal Numba taramasından farklı bir yöntem kullanıyor:

1. **Segmentli elek:** p ≤ √(N+1) asalları için n'nin düzgün kısmının σ'sı **tam sayı** olarak hesaplanıyor (uint64; N ≤ 10¹¹ için σ(n) < 2⁶⁴).
2. **Kalan kofaktör:** Ya 1 ya da tek bir büyük asal q. Bu durumda σ(n) ∈ [S·(q+1), S·(q+G)] tam sayı aralığına düşüyor. Kayan nokta kullanılmıyor.
3. **Filtre:** Aralıklar +2 farkıyla kesişmiyorsa n elenir.
4. **Aday kontrolü:** Adaylar 64-bit için deterministik Miller–Rabin ile tam hesaplanıyor. Bulunan ikizler bir de deneme bölmesiyle bağımsız olarak yeniden hesaplanıyor.

**G varsayımı:** q < 10¹¹ için ardışık asallar arasındaki en büyük boşluk 464'tür (Nicely'nin maksimal asal boşluk tabloları). Güvenlik payı olarak G = 1000 kullanılıyor. Bu varsayım yalnızca filtreyi etkiliyor.

```bash
gcc -O3 -march=native -fopenmp twins_c.c -o twins_c -lm
./twins_c 100000000000
```
