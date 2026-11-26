# 3. σ-ikizleri

**Tanım:** σ(n+1) = σ(n) + 2 sağlayan n'ler. Asal ikizlerinin (p, p+2) uzaylı karşılığı.

## Tam liste (10¹¹'e kadar, 22 terim)

| # | n | n çarpanları | n+1 çarpanları | σ(n) | σ(n+1) |
|---|---|---|---|---|---|
| 1 | 1 | 1 (∅) | 2 (a) | 1 | 3 |
| 2 | 2 | 2 (a) | 3 (b) | 3 | 5 |
| 3 | 14 | 2·7 (a·d) | 3·5 (b·c) | 33 | 35 |
| 4 | 25 | 5^2 (c^2) | 2·13 (a·f) | 49 | 51 |
| 5 | 94 | 2·47 (a·o) | 5·19 (c·h) | 159 | 161 |
| 6 | 142 | 2·71 (a·t) | 11·13 (e·f) | 219 | 221 |
| 7 | 214 | 2·107 (a·p28) | 5·43 (c·n) | 327 | 329 |
| 8 | 445 | 5·89 (c·x) | 2·223 (a·p48) | 679 | 681 |
| 9 | 574 | 2·7·41 (a·d·m) | 5^2·23 (c^2·i) | 1419 | 1421 |
| 10 | 1131 | 3·13·29 (b·f·j) | 2^2·283 (a^2·p61) | 2635 | 2637 |
| 11 | 2596 | 2^2·11·59 (a^2·e·q) | 7^2·53 (d^2·p) | 7137 | 7139 |
| 12 | 39224 | 2^3·4903 (a^3·p655) | 3·5^2·523 (b·c^2·p99) | 132543 | 132545 |
| 13 | 142708 | 2^2·35677 (a^2·p3795) | 7·19·29·37 (d·h·j·l) | 321561 | 321563 |
| 14 | 145863 | 3^2·19·853 (b^2·h·p147) | 2^3·18233 (a^3·p2090) | 492775 | 492777 |
| 15 | 181234 | 2·90617 (a·p8770) | 5·67·541 (c·s·p100) | 271857 | 271859 |
| 16 | 6915166 | 2·29·119227 (a·j·p11234) | 7·101·9781 (d·z·p1206) | 11088669 | 11088671 |
| 17 | 17768443 | 7·11·23·79·127 (d·e·i·v·p31) | 2^2·47·94513 (a^2·o·p9114) | 45090331 | 45090333 |
| 18 | 79906755 | 3·5·211·25247 (b·c·p47·p2786) | 2^2·83·101·2383 (a^2·w·z·p354) | 197099665 | 197099667 |
| 19 | 107246955 | 3·5·59·179·677 (b·c·q·p41·p123) | 2^2·83·107·3019 (a^2·w·p28·p433) | 263935105 | 263935107 |
| 20 | 811937494 | 2·405968747 (a·p21637601) | 5·211·269·2861 (c·p47·p57·p416) | 1217906247 | 1217906249 |
| 21 | 2573316475 | 5^2·23·4475333 (c^2·i·p314323) | 2^2·61·10546379 (a^2·r·p698459) | 6359473771 | 6359473773 |
| 22 | 76516058733 | 3·89·286576999 (b·x·p15563767) | 2·19·28807·69899 (a·h·p3137·p6928) | 138989849365 | 138989849367 |

Tüm liste: [`data/shift_twins_to_1e11.txt`](../data/shift_twins_to_1e11.txt)

1, 2, 14, 25, 94, 142, 214, 445, 574, 1131, 2596, 39224, 142708, 145863, 181234, 6915166, 17768443, 79906755, 107246955, 811937494, 2573316475, 76516058733

## Yöntem

1. **Logaritmik filtre:** log σ(n) − log σ(n+1) farkı titiz bir aralık hesabıyla 0'a yeterince yakın değilse n elenir. Büyük kofaktörler için [log(q+1), log(q+1000)] aralığı kullanılır.
2. **Kesin kontrol:** Adaylar iki büyük asal modül (2³¹−1 ve 2147483629) üzerinden tam hesapla doğrulanır. Sonraki asal, Miller–Rabin ile bulunur.
3. **Altyapı:** Google Colab, Numba.

Lean'de ayrıca kontrol edildi: `twins_ok` (22 terim) ve `twins_complete_3000` (3000'e kadar liste tam).

## Model ve sanı

- Teorem 3.3'teki tekil seri modeli d = 2 için yerel çarpan S ≈ 1,905 veriyor.
- Tahmin: N'ye kadar σ-ikizi sayısı ≈ **0,55 · ln N**.
- Test: 10⁵ ile 10¹¹ arasında beklenen 7,6 ± 2,8, gözlenen 10.

**Sanı:** σ-ikizleri sonsuz çoktur ve sayıları ~ c·ln N büyür (c ≈ 0,55).

Bunlar asal ikizlerinden çok daha seyrek (logaritmik büyüme), ama aynı türden bir "duvar"ın arkasındalar.
