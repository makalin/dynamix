# DynaMix

**DynaMix**, DJ'ler ve müzik tutkunları için tasarlanmış, iki MP3 dosyası arasındaki geçişlerde dinleyici enerjisinin korunmasına yardımcı olan bir ses analiz aracıdır. RMS (Root Mean Square) enerji seviyelerini analiz ederek, parçalardaki en uygun miksaj noktalarını belirler ve dans pistindeki enerjinin sabit kalmasını sağlar.

## Özellikler

- **Ses Enerjisi Analizi:** Her iki parça için RMS enerji değerlerini hesaplar.
- **Geçiş Noktası Tespiti:** İkinci parçanın enerjisinin önemli ölçüde arttığı noktayı belirler.
- **Miksaj Önerileri:** İlk parçanın enerjik kısmının ne kadar süre kullanılabileceğine dair öneriler sunar.
- **Görselleştirme:** Geçişin daha iyi anlaşılması için her iki parçanın enerji eğrilerini grafik olarak gösterir.

## Gereksinimler

- **Python 3.x**
- [Librosa](https://librosa.org/) – Ses işleme için.
- [NumPy](https://numpy.org/) – Sayısal işlemler için.
- [Matplotlib](https://matplotlib.org/) – Görselleştirme için.
- MP3 dosyalarını desteklemek için **FFmpeg** veya **AVbin** (gerektiğinde).

## Kurulum

1. **Depoyu Klonlayın veya İndirin:**

   ```bash
   git clone https://github.com/makalin/dynamix.git
   cd dynamix
   ```

2. **Gerekli Python Paketlerini Yükleyin:**

   ```bash
   pip install librosa numpy matplotlib
   ```

3. **FFmpeg'i Yükleyin (Eğer Yüklü Değilse):**

   - **FFmpeg İndir:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Alternatif olarak, işletim sisteminize uygun `apt`, `brew` veya `chocolatey` gibi paket yöneticilerini kullanabilirsiniz.

## Kullanım

DynaMix aracını, analiz etmek istediğiniz iki MP3 dosyasının yolunu belirterek komut satırından çalıştırabilirsiniz:

```bash
python mix_analiz.py yol/Parca1.mp3 yol/Parca2.mp3 --gecis_suresi 10 --threshold_factor 1.2
```

### Komut Satırı Argümanları

- **`yol/Parca1.mp3`**  
  İlk MP3 dosyasının yolu (örneğin, Tarkan'ın "Öp" şarkısı).

- **`yol/Parca2.mp3`**  
  İkinci MP3 dosyasının yolu (örneğin, Ajda Pekkan'ın "Harika" şarkısı).

- **`--gecis_suresi`** (Opsiyonel)  
  Parça 1'in son kaç saniyesinin analiz edileceğini belirtir.  
  _Varsayılan: 10 saniye_

- **`--threshold_factor`** (Opsiyonel)  
  Parça 2'deki enerji artışını tespit etmek için kullanılacak eşik çarpanı.  
  _Varsayılan: 1.2_

## Nasıl Çalışır?

1. **Ses Yükleme:**  
   Her iki MP3 dosyası Librosa kullanılarak yüklenir ve mono formata dönüştürülür.

2. **Enerji Hesaplama:**  
   RMS enerji değeri, parça bazında karekök ortalaması (RMS) yöntemiyle hesaplanarak dinamik seviyeler ölçülür.

3. **Geçiş Analizi:**  
   - Parça 1'in son birkaç saniyesindeki ortalama enerji değeri hesaplanır.
   - Parça 2 için, başlangıçtaki düşük enerjiden belirli bir kat (threshold_factor) kadar yüksek değerin elde edildiği ilk an tespit edilir.

4. **Görselleştirme:**  
   Her iki parçanın enerji eğrileri çizilir; grafik üzerinde:
   - Parça 1'in geçiş bölgesinin başlangıç noktası,
   - Parça 2'deki enerji artış noktası işaretlenir.

5. **Miksaj Önerisi:**  
   Yapılan analiz sonucunda, DynaMix, parça 1'in enerjik bölümünün ne kadar süreyle kullanılmasının uygun olacağına dair öneriler sunar.

## Özelleştirme

Miksaj tarzınıza uygun şekilde aşağıdaki parametreleri ayarlayabilirsiniz:
- **`--gecis_suresi`:** Parça 1'in son bölümünde analiz edilecek sürenin uzunluğunu belirleyin.
- **`--threshold_factor`:** Parça 2'de enerji artış tespitinin hassasiyetini ayarlayın.

## Lisans

Bu proje MIT Lisansı kapsamında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakınız.

## Teşekkürler

- [Librosa](https://librosa.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

---

DynaMix ile geçişlerinizde enerjiyi koruyun ve miksajlarınızın akıcılığını artırın!
