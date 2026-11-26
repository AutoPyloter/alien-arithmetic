# Kod

Python 3.10+. Gerekenler: `pip install -r requirements.txt`

Bazı betikler, depoda bulunmayan büyük asal tablolarını kullanır (`P.npy`: 10⁸'e kadar asallar, `P9.npy`: 10⁹'a kadar). Bunları `sympy.primerange` ya da `primesieve` ile üretebilirsiniz.

## `sigma/` — kaydırma haritası σ

| Dosya | İçerik |
|---|---|
| `alien_aliquot.py` | s(n) = σ(n) − n dizilerinin küçük ölçekli kaderi |
| `alien_aliquot2.py` | Hafızalı tam tarama: `python alien_aliquot2.py 10000000` → döngüler, tepe, en uzun yol |
| `sigtw.py`, `sigtw9.py`, `tw9.py` | σ-ikizi aramaları (yerel sürümler; 10¹¹ taraması Colab'de Numba ile yapıldı) |
| `fam.py` | D(n) = d aileleri ve tekil seri modeli testi |
| `newops.py` | Uzaylı işlemleri: ⊛ (harf polinomu çarpımı), ∂ (türev), ⊛-asallar |
| `alien_qs.py` | Uzaylının kendi problemleri |

## `exploration/` — ilk keşif turu

Çalışmanın erken safhasındaki deneme betikleri. Yorumlar Türkçe; bazıları yanlışlanmış hipotezleri test eder (sonuçlar `notes/uzayli_defteri.md` içinde).

| Grup | Dosyalar | Konu |
|---|---|---|
| Uzaylı alfabesi | `alien*.py` | harf büyümesi, yeni harf olasılığı |
| Hipotez testleri | `h*.py` | Goldbach yol sayısı (H6, H7), komşu yasaları (H8, H9), Collatz tepe (H10, H11), log₂3 yaklaşımları (H13) |
| Gece hedefleri | `g*.py` | G3–G15 hedefleri (Bateman–Horn, rad grupları, tırmanış sistemleri) |
| Parite duvarı | `par*.py`, `blk.py`, `t2.py`, `omega.py` | Liouville korelasyonları, Selberg sahte dizileri |
| Collatz | `t3.py`, `t5.py`, `h3.py` | uzaylı formunda Collatz, Baker tablosu |
| Tünel | `tunnel*.py` | iki taraftan kazma deneyleri |
| Diğer | `perfect.py`, `zero.py`, `spec9.py`, `star_pnt.py`, `curve.py`, `gaps.py`, `mk.py` | mükemmel sayılar, zeta sıfırları spektrumu, ⊛-PNT, GPY |
