# Su, Kum ve Hücre uygarlıkları

Üç uygarlık sayıya üç farklı yoldan bakıyor. Su uygarlığı döker ve ölçer. Kum uygarlığı atar ve sayar. Hücre uygarlığı sayı bilmez, yalnızca komşusuna bakar. Her birinde bazı şeyler bedava, bazıları imkânsıza yakın. Zorluk kaybolmuyor, yer değiştiriyor.

Kod bu klasörde. Çıktılar `*_cikti.txt` dosyalarında. Bütün iddialar aşağıdaki aralıklarda sayısal olarak test edildi.

| Dosya | İçerik |
|---|---|
| `su.py`, `su_olcek.py` | BFS, kapalı form, Sylvester, 3 kap Dijkstra, Arnold ölçeklemesi |
| `pi_digits.py`, `kum.py` | π'nin 10⁶ basamağı (mpmath), Buffon, Monte Carlo, ki-kare |
| `hucre.py` | Collatz hücresel otomatı (taban 6), De Mol etiket sistemi, Kural 30/110, Yaşam |
| `lean/Frobenius.lean`, `lean/Hucre.lean` | Çekirdek Lean 4.15 ispatları (Mathlib yok, `sorry` yok) |

---

## 1. Su uygarlığı: kaplar

### Notasyon

Bir sayı, iki kapla yapılan bir dökme dizisidir. "4" demek, "3 ve 5 litrelik kapla 4 litreyi ölçen en kısa dizi" demektir. Durum (x, y) çiftidir. Altı hamle var: doldur, boşalt, birinden ötekine dök.

### Yasalar

| Yasa | Test | Sonuç |
|---|---|---|
| **Bézout:** c litre ölçülür ⇔ c ≤ b ve ebob(a,b) \| c | 1 ≤ a ≤ b ≤ 30, tüm c | 9920 durum, 0 hata |
| **İki saf strateji yeter:** en kısa dizi = min(A→B stratejisi, B→A stratejisi) | a, b ≤ 30 | 6804 durum, 0 hata |
| **Kapalı form** (aşağıda) | a < b ≤ 30 (tam BFS) ve rastgele 200 çift b ≤ 150 | 0 hata |
| **Sylvester:** aralarında asal a, b için en büyük elde edilemez miktar ab − a − b | 2 ≤ a < b ≤ 40 | 0 hata |
| 3 kap: Dijkstra (mod a en kısa yol) = kaba kuvvet | a < b < c ≤ 25, 1741 üçlü | 0 hata |
| **Davison alt sınırı:** F ≥ √(3abc) − a − b − c | 50 000 rastgele üçlü, N ≤ 10⁵ | 0 ihlal; en küçük (F+a+b+c)/√(abc) = 1,7348 (√3 = 1,7321) |
| **Arnold/Ustinov:** (F+a+b+c)/√(abc) ortalaması → 8/π ≈ 2,5465 | bkz. tablo | uyumlu |

**Kapalı form.** a < b aralarında asal, 0 < c < b, c ≠ a olsun.
- A→B (küçükten büyüğe dök): x ≥ 1 en küçük sayı, x·a ≡ c (mod b); y = (xa − c)/b. Adım = 2(x+y) − 2·[c < a].
- B→A (büyükten küçüğe dök): x' ≥ 1 en küçük sayı, x'·b ≡ c (mod a); y' = (x'b − c)/a. Adım = 2(x'+y') − 2.
- En kısa dizi bu ikisinin küçüğü. c = a ise 1 adım.

Örnek: 3 ve 5 ile 4 litre. A→B: x = 3, y = 1, 8 adım. B→A: x' = 2, y' = 2, 6 adım. Die Hard bulmacasının cevabı 6.

**Arnold ölçeklemesi** (rastgele üçlüler, a, b, c ≤ N, ebob = 1):

| N | örnek | ortalama | medyan | en büyük |
|---|---|---|---|---|
| 10³ | 20 000 | 2,463 ± 0,010 | 2,043 | 22,4 |
| 10⁴ | 20 000 | 2,538 ± 0,014 | 2,040 | 51,0 |
| 10⁵ | 4 000 | 2,564 ± 0,041 | 2,041 | 93,3 |

Ortalama 8/π'ye yaklaşıyor. Dağılımın kuyruğu kalın, bu yüzden ortalama yavaş oturuyor. En büyük değer N ile büyüyor.

### Kolay / Zor

| Su uygarlığı için kolay | Su uygarlığı için zor |
|---|---|
| ebob (kaplar sadece ebob'un katlarını ölçer) | Asallık: kap dilinde "asal" kavramı yok |
| İki kap Frobenius: ab − a − b, tek formül | Üç kap Frobenius: kapalı polinom formül yok |
| En kısa dökme dizisi: iki modüler ters ile | n kap Frobenius: n serbest olunca NP-zor |
| Bézout katsayıları (dökme sayıları) | Kare kök, π gibi ölçülemeyen büyüklükler |

### Doğal açık problem

Üç kap için kapalı form yok. Curtis (1990), Frobenius sayısının üç üreteçte sonlu sayıda polinomla ifade edilemeyeceğini gösterdi. Hızlı algoritmalar var (Selmer–Beyer, Rødseth, Greenberg; sürekli kesirle). Sabit sayıda kap için polinom zamanlı algoritma var. Kap sayısı serbestse problem NP-zor. Dört ve daha fazla kap için genel formül bilinmiyor.

### Yeni gözlemler

1. **En zor miktar sınırı.** M(a,b), en zor c için en kısa dizinin uzunluğu olsun. Gözlem: a < b aralarında asal ve b ≥ 5 için **M(a,b) ≤ 2(b − 2)**. Eşitlik ancak **b − a = 1** veya **b − a = 2 ve a tek** iken. Test: b ≤ 150, 6852 çift, 0 ihlal, istisnasız 219 eşitlik. Örnek: (29, 30) ile c = 15, 56 adım. Yenilik notu: Kapalı formun "iki saf strateji" kısmı folklor (programlama bulmaca sitelerinde aynı simülasyon var). Maksimum için bu sınırı ve eşitlik durumlarını taradığımız kaynaklarda göremedik. Kapalı formdan kısa bir ispatı olması muhtemel. Bilinen bir sonuç olabilir.
2. **Medyan sabit görünüyor.** (F+a+b+c)/√(abc) için medyan üç ölçekte de 2,04 civarında. Ortalama kuyruk yüzünden oynuyor. Yenilik notu: Bu tek bir gözlem. Üç üreteçli Frobenius sayısının limit dağılımı literatürde çalışılmış (Ustinov, Marklof; Shur–Sinai–Ustinov). Medyan o dağılımdan hesaplanabilir. Biz karşılaştırmadık.

---

## 2. Kum uygarlığı: at ve say

### Notasyon

Bir sayı, bir atış deneyinin oranıdır. π, "iğnenin çizgiyi kesme sıklığı"ndan çıkar: P = 2l/(πt). Kum uygarlığı π'yi bilmeden de iğneyi atabilir. Kodda yön bile π kullanmadan üretildi (birim diskten reddetme örneklemesi).

### Yasalar

| Yasa | Test | Sonuç |
|---|---|---|
| Buffon: π̂ = 2lN / (t·kesen) | N = 10² … 10⁷ | 10⁷ atışta hata 3·10⁻⁴ |
| **Hata ∝ 1/√N**, sabit √(π²(π−2)/2) ≈ 2,374 (l = t) | 400 tekrar, N = 10² … 10⁵ | RMS·√N = 2,51; 2,41; 2,23; 2,45 |
| Monte Carlo hacim, d boyutlu top | 10⁶ nokta, d = 2 … 20 | d = 2'de 5·10⁻⁴ göreli hata; d = 15'te 11 isabet; d = 20'de 0 isabet |
| π'nin ilk 10⁶ basamağı, rakam frekansı | ki-kare, sd = 9 | 5,51, p = 0,79 |
| İkili ve üçlü bloklar (örtüşmesiz) | sd = 99 ve 999 | p = 0,30 ve 0,50 |
| 100 parçanın (10⁴ basamak) p-değerleri | KS düzgünlük testi | p = 0,37 |

Rakam sayıları: 0: 99959, 1: 99758, 2: 100026, 3: 100229, 4: 100230, 5: 100359, 6: 99548, 7: 99800, 8: 99985, 9: 100106. Bilinen tabloyla aynı.

Lazzarini (1901): 3408 atış, l/t = 5/6, 1808 kesiş. Sonuç tam olarak 355/113. Bu kadar iyi bir sonuç 1/√N yasasıyla uyuşmuyor. Deneyin sonucu "ayarlandığı" düşünülüyor. Kum uygarlığında hile bile yasayı ele veriyor.

### Kolay / Zor

| Kum için kolay | Kum için zor |
|---|---|
| Herhangi bir alan ya da hacim, şekil ne kadar karmaşık olursa olsun | Her ek basamak 100 kat atış ister (k basamak ≈ 10^(2k) atış) |
| İntegral, olasılık, ortalama | Yüksek boyut: d = 20 topu 10⁶ atışta hiç görülmüyor |
| "Rastgele görünüyor mu?" sorusu (ki-kare) | "Gerçekten rastgele mi?" sorusu: hiçbir sonlu test ispat değil |

### Doğal açık problem

**π normal mi?** Yani her k uzunluklu basamak dizisi 10^(−k) sıklıkla mı çıkıyor? Bilinmiyor. Doğal hiçbir sabit için, tek bir tabanda bile normallik ispatlanmış değil. Bailey ve Crandall, π'nin 2 tabanında normalliğini "Hypothesis A" adlı kaotik dinamik varsayımına indirdi. Varsayım açık. Kum uygarlığı π'nin basamaklarını sonsuza kadar sayabilir ama normalliği hiçbir zaman ispatlayamaz.

### Yeni gözlem denemesi

**Tüm k-basamaklı dizilerin tamamlanma anı.** π'de bütün 10^k dizi ilk kez kaçıncı basamakta görülmüş oluyor? Bunu rastgele basamak dizileriyle karşılaştırdık (kupon toplayıcı problemi).

| k | π'de tamamlanma | rastgele ortalama ± SD | π'nin yüzdelik sırası |
|---|---|---|---|
| 2 | 606 | 527 ± 118 | 0,78 |
| 3 | 8555 | 7480 ± 1288 | 0,82 |
| 4 | 99 849 | 96 458 ± 12 359 | 0,72 |

π üç ölçekte de biraz geç tamamlıyor. Ama hepsi bir standart sapma içinde. Anlamlı bir sapma yok. Yenilik notu: Bu bir "rastgelelik testi" sadece. Benzer testler (boşluk, kupon toplayıcı) Knuth'un listesinde var. π için yeni bir şey söylemiyor. Normallikle tutarlı.

---

## 3. Hücre uygarlığı: sadece komşuya bak

### Notasyon

Sayı yok. Bir hücre dizisi var. Her hücre her adımda yalnızca kendine ve iki komşusuna bakıp yeni durumunu seçer. Sayı, bir desenin "adı"dır.

### Collatz'ı hücrelerle yazmak

**Kodlama 1: taban-6 otomatı (Kari'nin fikri).** Hücreler taban-6 rakamı tutar, birler basamağında bir "nokta" işareti var. 12 durum, yarıçap 1. Kural:
- Herkes 3 ile çarpar: yeni rakam = 3·(kendi mod 2) + ⌊sağ komşu / 2⌋. 3, 6'yı böldüğü için elde (taşıma) yok. Bu tamamen yerel.
- Birler hücresi tekse 3 olur, sonra 4 yapılır: 3n + 1.
- Birler hücresi çiftse 0 olur, nokta bir sola kayar: 3n/6 = n/2.

Çift/tek kararı global görünür, ama sadece birler hücresinde verilir. Kural tablosu 12³ = 1728 girdili sabit bir tablo.

**Kodlama 2: De Mol etiket sistemi.** Harfler {a, b, c}. Her adımda ilk harfe bak, ilk iki harfi sil, kurala göre sona ekle: a → bc, b → a, c → aaa. aⁿ kelimesi a^T(n) kelimesine gider, T(n) = n/2 (çift) ya da (3n+1)/2 (tek).

| Yasa | Test | Sonuç |
|---|---|---|
| Taban-6 otomatı Collatz'ı adım adım hesaplar | n ≤ 3000, 215 063 adım | 0 hata. Lean: her n için ispat |
| De Mol sistemi aⁿ → a^T(n) | 2 ≤ n ≤ 5000 | 0 hata. Lean: n ≤ 100, `decide` |
| Bir T-adımı = n + (n mod 2) etiket adımı | 2 ≤ n ≤ 5000 | doğru (kendi gözlemimiz, kolay) |
| Kural 30 merkez sütunu | 10 001 bit | 1 oranı 0,503; son 4000 bitte ≤ 2000 periyot yok |
| Yaşam Oyunu planörü | 4 adım | çapraz bir hücre kaymış kopya |
| {(3/2)^t} kesirli kısımları | t ≤ 3000 | KS düzgünlük p = 0,96 |

### Kolay / Zor

| Hücre için kolay | Hücre için zor |
|---|---|
| ×3 (taban 6'da yerel, elde yok) | Toplama: elde zinciri bütün diziye yayılabilir |
| Collatz'ın bir adımı | Collatz'ın sonunda 1'e varıp varmadığı |
| Evrensel hesap (Kural 110, Yaşam Oyunu) | Uzun vadeli davranışı öngörmek (karar verilemez) |
| Rastgele görünen desen üretmek (Kural 30) | Bu desenin periyodik olmadığını ispatlamak |

### Karar verilemezlik: Conway ve FRACTRAN

Conway (1972) Collatz'ı genelleştirdi. Fonksiyon parçalı doğrusal: n'nin kalan sınıfına göre g(n) = aᵢ·n + bᵢ. Bu tür bir fonksiyonu tekrar tekrar uygulamak her hesabı taklit edebilir. FRACTRAN bunun özel hâli: bir kesir listesi var; n'yi listede tam sayı veren ilk kesirle çarp. Bu dil evrensel. Bu yüzden "verilen genelleştirilmiş Collatz oyunu 1'e varır mı?" sorusu, durma problemi kadar zordur. Genel olarak çözen bir algoritma yoktur. Kurtz ve Simon (2007) daha da ileri gitti: "her başlangıç 1'e varır mı" sorusu Π⁰₂-tamdır. Bu, gerçek 3n+1 probleminin karar verilemez olduğunu **göstermez**. Sadece ailesinin genel üyesinin öyle olduğunu gösterir. Conway, kendi örneğinde doğru ama ispatlanamaz önermeler kurdu.

Hücre uygarlığı açısından aynı resim: Kural 110 evrensel (Cook). Etiket sistemleri evrensel. Collatz bu dillerin içine birkaç satırla sığıyor. Sığması onu çözmüyor.

### Doğal açık problemler

- **Collatz:** Her n sonunda 1'e varır mı? Hücre dilinde: taban-6 otomatında her sonlu desen tek bir "1" desenine varır mı? Açık.
- **Kural 30 (Wolfram'ın 2019 ödül problemleri):** Merkez sütun sonunda periyodik olur mu? Siyah ve beyaz oranı 1/2'ye mi gider? n. biti hesaplamak lineer zamandan az olabilir mi? Üçü de açık. 2026 tarihli bir ön baskı yalnızca "sonunda sabit olma" durumunu sonlu başlangıçlar için dışlıyor. Ön baskının kendisi Problem 1'i çözmediğini söylüyor.
- **Mahler problemi:** Kari'nin ×3/2 otomatı (3/2)^t'nin kesirli kısımlarına bağlı. {ξ(3/2)^t} her zaman 1/2'nin altında kalan bir ξ > 0 var mı? Açık.

### Yeni gözlem denemesi

**×3 bedava, +1 tek hücrede.** Taban 6'da Collatz'ın "zor" kısmı aritmetik değil. ×3 elde üretmez. +1 hiç taşmaz (son basamak 3 → 4). /2 de sadece noktayı kaydırır. Bütün zorluk, noktanın hangi yöne gittiğini veren **tek bir bitlik** yerel karara toplanıyor. Lean'de genel ispat var (`caStep_correct`). Yenilik notu: Bu, Kari'nin (2012) kurgusunun yeniden ifadesi. Yeni olan sadece formal ispat. Literatürde benzer gözlemler var ("Collatz taban 6'da hücresel otomattır").

---

## Lean sonuçları

Derleyici: Lean 4.15.0, çekirdek, Mathlib yok. `sorry` yok. Somut kontroller çekirdek `decide` ile yapıldı. `native_decide` kullanılmadı.

**`lean/Frobenius.lean`** (Su)
- `sylvester_gap`: **Genel.** a, b > 0 ve ebob(a,b) = 1 ise ab − a − b, ax + by biçiminde yazılamaz. Her a, b için.
- `all_above`: **Genel.** F+1, …, F+a hepsi elde edilebilirse F'den büyük her sayı elde edilir.
- `allPairs_spec`: 2 ≤ a < b ≤ 12, ebob = 1 olan bütün çiftlerde tam Sylvester: ab − a − b elde edilemez ve ondan büyük her sayı (sonsuz çok) elde edilir.
- `su_3_5`, `su_4_7`, `su_5_8`, `su_7_11`: somut örnekler. `su_4_6_odd`: 4 ve 6 ile hiçbir tek sayı elde edilmez.
- Eksik: "her büyük sayı elde edilir" kısmının **genel** ispatı. Bu Bézout ya da güvercin yuvası ister. Mathlib'siz yazmadık.

**`lean/Hucre.lean`** (Hücre)
- `val_times3`: **Genel.** Yerel kural "yeni rakam = 3(d mod 2) + ⌊önceki/2⌋" değeri tam 3 ile çarpar.
- `times3_digits`: Girdi rakamları < 6 ise çıktı rakamları da < 6 (elde yok).
- `caStep_correct`: **Genel.** Otomatın bir adımı, her n için Collatz'ın bir adımına eşit.
- `tag_ok_100`: De Mol etiket sistemi 2 ≤ n ≤ 100 için aⁿ → a^T(n).

`#print axioms` çıktısı:

```
'allPairs_spec' depends on axioms: [propext, Quot.sound]
'sylvester_gap' depends on axioms: [propext, Quot.sound]
'all_above' depends on axioms: [propext, Quot.sound]
'su_3_5' depends on axioms: [propext, Quot.sound]
'su_7_11' depends on axioms: [propext, Quot.sound]
'allPairs_ok' depends on axioms: [propext]
'su_4_6_odd' depends on axioms: [propext, Quot.sound]
'val_times3' depends on axioms: [propext, Quot.sound]
'times3_digits' depends on axioms: [propext, Quot.sound]
'caStep_correct' depends on axioms: [propext, Quot.sound]
'tag_ok_100' does not depend on any axioms
```

`Classical.choice` yok, `sorryAx` yok, `Lean.ofReduceBool` yok.

---

## Kaynaklar

- J. J. Sylvester (1882/1884); "Coin problem", Wikipedia: https://en.wikipedia.org/wiki/Coin_problem (n = 2 formülü; n > 2 için kapalı form yok; sabit n için polinom algoritma; n serbestken NP-zor).
- F. Curtis, "On formulas for the Frobenius number of a numerical semigroup", *Math. Scand.* 67 (1990) 190–192: https://geodesic.mathdoc.fr/item/MS2_1990__67_2_167131 (özetini görmedik; içerik literatürdeki atıflardan).
- I. Aliev, P. Gruber, "An optimal lower bound for the Frobenius problem": https://arxiv.org/abs/math/0512083 (Davison 1994 alt sınırı √(3abc) − a − b − c; Selmer–Beyer, Rødseth, Greenberg).
- A. V. Ustinov, "The solution of Arnold's problem on the weak asymptotics of Frobenius numbers with three arguments", *Sb. Math.* 200 (2009): https://ui.adsabs.harvard.edu/abs/2009SbMat.200..597U (ortalama (8/π)√(abc)).
- C. Lalov, "A new approach for solving the generalized 2 jugs decanting problem", *Parabola* 52(1) (2016): https://parabola.unsw.edu.au/sites/default/files/2024-03/vol52_no1_3.pdf
- Su kabı bulmacası, Bézout ve BFS: https://raw.org/puzzle/misc/solution-to-the-water-jug-problem/
- D. H. Bailey, R. Crandall, π'nin normalliği ve "Hypothesis A" (LBL, 2001): https://www2.lbl.gov/Science-Articles/Archive/pi-random.html
- J. Kari, "Cellular Automata, the Collatz Conjecture and Powers of 3/2", DLT 2012; slaytlar: https://www.ci2ma.udec.cl/disco/slides/discoKari.pdf
- "Tag system", Wikipedia (De Mol'ün Collatz etiket sistemi; Cook, Kural 110): https://en.wikipedia.org/wiki/Tag_system
- J. H. Conway, "On unsettleable arithmetical problems" (Amer. Math. Monthly 2013; 1972 "Unpredictable iterations" sonucunun anlatımı): https://www.gwern.net/doc/cs/computable/2013-conway.pdf
- J. Endrullis, C. Grabmayer, D. Hendriks, "Complexity of Fractran and Productivity" (Kurtz–Simon Π⁰₂-tamlığı): https://arxiv.org/abs/0903.4366
- Rule 30 Prize Problems, MathWorld: https://mathworld.wolfram.com/Rule30PrizeProblems.html
- D. L. Condrey, "Finite Configurations Cannot Generate a Constant Trace in Rule 30", arXiv:2609.09431 (2026): https://arxiv.org/abs/2609.09431
