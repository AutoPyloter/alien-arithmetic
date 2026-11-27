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

## Hesap (`code/spoof/descartes_squares.c`)

- Her tek m için σ(m²)'yi parçalı elekle hesaplıyor (128 bit tam sayılar).
- d = 2m² − σ(m²) > 0 ve d ∣ σ(m²) koşulunu kontrol ediyor; sağlanıyorsa x = σ(m²)/d.
- Doğrulama: m ≤ 20 000 için Python + sympy ile kaba hesap aynı sonucu veriyor. Ayrıca m ≈ 10¹¹ civarında rastgele 100 değerde σ(m²) sympy ile birebir aynı.

| aralık | süre (2 çekirdek) | bulunan |
|---|---|---|
| m ≤ 10⁶ (n ≤ 10¹², Tóth'un sınırı) | 0,05 s | yalnızca m = 3003, x = 22021 (Descartes) |
| m ≤ 10⁹ (n ≤ 10¹⁸) | 26 s | yalnızca Descartes |
| m < 10¹¹ (n < 10²²) | yaklaşık 47 dk | yalnızca Descartes |

**Yeni sınır:** Descartes örneği dışında bir Descartes sayısı D = n·x varsa **n > 10²²**. Bu, Tóth'un 10¹² sınırının on milyar (10¹⁰) kat büyütülmesi. Ham çıktı: `data/descartes_squares_m_1e11.txt`.

## Notlar

- Bu tanım n ile x'in aralarında asal olmasını şart koşmuyor (Tóth'un tanımı). Dittmer'in yarı-asal çarpan tanımı daha genel ama farklı bir sayım kullanıyor; bu sonuç onun "7 çarpan" sorusunu çözmüyor.
- Gözlem çok basit olduğu için literatürde başka bir yerde geçiyor olabilir. Ancak Tóth'un taraması bunu kullanmamış ve 2025'te de 10¹² sınırı anılıyor.
