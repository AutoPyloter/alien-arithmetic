# 18. Descartes sayıları: Tóth'un 10¹² sınırını aşmak

**Soru:** Descartes'ın 1638 örneği D = 3²·7²·11²·13²·22021 dışında tek bir "sahte mükemmel sayı" (Descartes sayısı) var mı?

**Tanım (Tóth 2021, 2025):** Tek n ve tek x ≥ 2 için

  σ(n)·(x + 1) = 2·n·x    (denk biçim: 2n/σ(n) − 1 = 1/x)

ise D = n·x bir Descartes sayısıdır. x asal olsaydı D gerçek bir tek mükemmel sayı olurdu.

**Bilinen en iyi sınır:** Tóth (2021), Descartes örneği dışında bir D = n·x varsa n > 10¹² olduğunu gösterdi. Bunun için bütün tek n ≤ 10¹² taranmıştı. Tarama 6 çekirdekli bir işlemcide yaklaşık 8 ay sürdü ve hiçbir kısıt kullanılmadı. Tóth'un 2025 makalesi de bu sınırı hâlâ en iyi sınır olarak anıyor.

## Gözlem: n tam kare olmak zorunda

n ve x tek olsun.
- Sağ taraf 2nx ≡ 2 (mod 4).
- Sol tarafta x + 1 çift. Çarpım ≡ 2 (mod 4) olduğuna göre σ(n) tek olmalı ve x ≡ 1 (mod 4).
- n tek ve σ(n) tek ⇒ n tam kare (klasik: σ(n) tek ⇔ n kare ya da iki kere kare).

**Sonuç:** n = m². Dolayısıyla "n ≤ 10¹²" taraması aslında yalnızca "tek m ≤ 10⁶" demek. Bu, Euler'in tek mükemmel sayılar için kullandığı mod 4 argümanının sahte sayılardaki karşılığı. Harf dilinde: n'nin harf vektöründe bütün üsler çift; tek üslü tek harf, sahte çarpan x.

## İkinci gözlem: açık (2n − σ(n)), n'yi böler

d = 2n − σ(n) olsun. Eşitlik σ(n)·x + σ(n) = 2n·x biçiminde yazılınca:
- **σ(n) = x·d.**
- **(x + 1)·d = 2n.** Buradan x + 1 = 2k (k tam sayı) için **k·d = n**, yani **d ∣ n**.
- Dolayısıyla **σ(n)/n = 2 − 1/k**: n'nin bolluk oranı 2'nin tam olarak bir birim kesir kadar altında. x ≡ 1 (mod 4) olduğundan k tek.

Descartes örneği: n = 3003², d = 819, k = 11011, x = 22021 = 2k − 1.

## Üçüncü ve dördüncü gözlem: bolluk en az 5/3

- **Teorem 3.** n tek olduğundan k tek, dolayısıyla x = 2k − 1 ≡ 1 (mod 4) ve x ≥ 5. Buradan k ≥ 3 ve **σ(n)/n = 2 − 1/k ≥ 5/3**.
- **Teorem 4.** σ(m²)/m² < ∏_{p ∣ m} p/(p−1) olduğundan **∏_{p ∣ m} p/(p−1) > 5/3**.

Bu çok güçlü bir filtre. 3 ∤ m ise m'nin en az dört asalı olmalı (örneğin 5·7·11·13). 3 ∣ m ise 5 ya da 7 de m'yi bölmeli; ikisi de bölmüyorsa birkaç ek asal gerekiyor.

**Çekirdek taraması (`code/spoof/descartes_cores.c`).**
- m'nin asallarını artan sırada dizince, p/(p−1) çarpımının ilk kez eşiği aştığı önek C "çekirdek" olsun ve m = c·t.
- t'nin her asalı ya C'de ya da C'nin en büyük asalından büyük. Her m en fazla bir çekirdeğe düşer.
- Eşik (5/3)(Q−1)/Q alınıyor. Q = max(√B, 2·10⁶) olduğundan m'nin Q'dan büyük en fazla bir asalı olabilir, o yüzden bütün çekirdek asalları Q'nun altında kalıyor.

Sonuç: tek m'lerin yalnızca yaklaşık %14'ü taranıyor ve tarama 7 kat hızlanıyor.

**Doğrulama.**
- Kapsama testi: m < 3·10⁵'te Teorem 4'ü sağlayan 17 994 adayın her biri tam bir kez taranıyor (eksik 0, fazla 0, tekrar 0) ve σ değerleri sympy ile aynı.
- Tutarlılık: m < 10¹¹ için iki program (düz tarama ve çekirdek taraması) aynı sonucu veriyor.

## Lean'de (`lean/Descartes.lean`, Mathlib yok, standart aksiyomlar)

| Teorem | İçerik |
|---|---|
| `descartes_square` | tek n, tek x, σ(n)(x+1) = 2nx ⇒ n tam kare |
| `descartes_deficiency` | aynı koşullarda σ(n) = x·d, (x+1)·d = 2n, d ∣ n |
| `descartes_abundancy` | x ≡ 1 (mod 4), x ≥ 5 ve 5n ≤ 3σ(n) (Teorem 3) |
| `descartes_core` (`lean/DescartesCore.lean`) | n = ∏ p^(e p) ise 5·∏(p − 1) < 3·∏p, yani ∏ p/(p−1) > 5/3 (Teorem 4) |

Böylece taramanın dayandığı bütün matematik (n kare, d ∣ n, bolluk ≥ 5/3, ∏ p/(p−1) > 5/3) biçimsel olarak doğrulandı. Geriye yalnızca hesap (C programı) kalıyor.

## Hesap (`code/spoof/descartes_squares.c`)

- Her tek m için σ(m²)'yi parçalı elekle hesaplıyor (128 bit tam sayılar, yalnızca tek m'ler; ilk sürüme göre 2,2 kat hızlı).
- d = 2m² − σ(m²) > 0 ve d ∣ σ(m²) koşulunu kontrol ediyor; sağlanıyorsa x = σ(m²)/d.
- Doğrulama: m ≤ 20 000 için Python + sympy ile kaba hesap aynı sonucu veriyor. Ayrıca m ≈ 10¹¹ civarında rastgele 100 değerde σ(m²) sympy ile birebir aynı.

| aralık | süre (2 çekirdek) | bulunan |
|---|---|---|
| m ≤ 10⁶ (n ≤ 10¹², Tóth'un sınırı) | 0,05 s | yalnızca m = 3003, x = 22021 (Descartes) |
| m ≤ 10⁹ (n ≤ 10¹⁸) | 26 s | yalnızca Descartes |
| m < 10¹¹ (n < 10²²) | yaklaşık 47 dk | yalnızca Descartes |
| m < 10¹¹, çekirdek taraması (yeniden) | 3 dk | yalnızca Descartes (düz taramayla aynı) |
| 10¹¹ ≤ m < 10¹² (n < 10²⁴), çekirdek taraması | 25 dk | yok |

**Yeni sınır:** Descartes örneği dışında bir Descartes sayısı D = n·x varsa **n > 10²⁴**. Bu, Tóth'un 10¹² sınırının 10¹² kat büyütülmesi. Ham çıktılar: `data/descartes_squares_m_1e11.txt` ve `data/descartes_cores_m_1e12.txt`.

## Notlar

- Bu tanım n ile x'in aralarında asal olmasını şart koşmuyor (Tóth'un tanımı). Dittmer'in yarı-asal çarpan tanımı daha genel ama farklı bir sayım kullanıyor; bu sonuç onun "7 çarpan" sorusunu çözmüyor.
- Gözlem çok basit olduğu için literatürde başka bir yerde geçiyor olabilir. Ancak Tóth'un taraması bunu kullanmamış ve 2025'te de 10¹² sınırı anılıyor.
