# DynaMix

**DynaMix**, DJ'ler ve müzik tutkunları için tasarlanmış, gelişmiş ses geçiş analiz aracıdır. RMS (Root Mean Square) enerji seviyeleri, BPM, müzikal anahtar ve diğer ses özelliklerini analiz ederek, parçalardaki en uygun miksaj noktalarını belirler ve dans pistindeki enerjinin sabit kalmasını sağlar.

## 🚀 Yeni Özellikler

### Gelişmiş Analiz Araçları
- **BPM Tespiti:** Güvenilir tempo analizi ve güven skorlaması
- **Anahtar Tespiti:** Harmonik miksaj için müzikal anahtar belirleme
- **Vuruş Izgarası Analizi:** Hassas vuruş zamanlaması ve güç analizi
- **Bölüm Tespiti:** Intro, verse, chorus, bridge, outro otomatik belirleme
- **Drop Tespiti:** Enerji düşüşü ve yükseliş noktalarının belirlenmesi

### Playlist Yönetimi
- **Playlist Analizi:** Tüm müzik koleksiyonlarını analiz etme
- **Set Listesi Oluşturma:** DJ setleri için optimal parça sıralaması
- **Enerji Eğrisi Optimizasyonu:** Yükseliş, dalga veya özel enerji desenleri
- **Uyumluluk Matrisi:** Parça-parça uyumluluk skorlaması
- **Dışa/İçe Aktarma:** Playlist analizlerini kaydetme ve yükleme

### DJ Performans Araçları
- **Cue Noktası Tespiti:** DJ performansı için optimal cue noktaları
- **Döngü Önerileri:** Müzikal cümle ve bölüm tabanlı döngü önerileri
- **Performans Bölgeleri:** Intro, build, drop, breakdown, outro analizi
- **DJ Notları Oluşturma:** Her parça için kapsamlı performans notları
- **Toplu Analiz:** Tüm dizinleri otomatik işleme

### Gelişmiş Görselleştirme
- **Kapsamlı Grafikler:** Enerji profilleri, vuruş ızgaraları, kromagramlar
- **Uyumluluk Radar Grafiği:** Görsel uyumluluk skorlaması
- **Performans Bölgeleri:** Renk kodlu parça bölümleri
- **Cue Noktası Görselleştirmesi:** Onset gücü ve zamanlama analizi

## 📋 Gereksinimler

- **Python 3.8+**
- [Librosa](https://librosa.org/) – Ses işleme için
- [NumPy](https://numpy.org/) – Sayısal işlemler için
- [Matplotlib](https://matplotlib.org/) – Görselleştirme için
- [Pandas](https://pandas.pydata.org/) – Veri analizi için
- [Seaborn](https://seaborn.pydata.org/) – Gelişmiş grafik çizimi için
- MP3 dosyalarını desteklemek için **FFmpeg** veya **AVbin** (gerektiğinde)

## 🛠️ Kurulum

1. **Depoyu Klonlayın veya İndirin:**

   ```bash
   git clone https://github.com/makalin/dynamix.git
   cd dynamix
   ```

2. **Gerekli Python Paketlerini Yükleyin:**

   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg'i Yükleyin (Eğer Yüklü Değilse):**

   - **FFmpeg İndir:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Alternatif olarak, işletim sisteminize uygun `apt`, `brew` veya `chocolatey` gibi paket yöneticilerini kullanabilirsiniz.

## 🎵 Kullanım

### Temel İki Parça Analizi

Orijinal DynaMix aracını temel enerji analizi için çalıştırın:

```bash
python mix_analiz.py yol/Parca1.mp3 yol/Parca2.mp3 --gecis_suresi 10 --threshold_factor 1.2
```

### Gelişmiş Analiz

Kapsamlı analiz için gelişmiş versiyonu kullanın:

```bash
python mix_enhanced.py parca1.mp3 parca2.mp3 --visualize
```

### Playlist Analizi

Tüm müzik koleksiyonlarını analiz edin:

```bash
python mix_enhanced.py --playlist /muzik/klasoru/yolu --set-duration 90 --visualize
```

### DJ Performans Araçları

Tekil parçalar için DJ notları oluşturun:

```bash
python dj_tools.py parca.mp3 --export dj_notlari.txt --visualize
```

Tüm dizinleri toplu analiz edin:

```bash
python dj_tools.py --batch /muzik/klasoru/yolu --output-dir /notlar/yolu
```

## 📊 Komut Satırı Argümanları

### Gelişmiş Mix Analizi (`mix_enhanced.py`)

- **`parca1`** - İlk MP3 dosya yolu
- **`parca2`** - İkinci MP3 dosya yolu
- **`--visualize`** - Gelişmiş görselleştirmeleri göster
- **`--playlist`** - Tüm playlist dizinini analiz et
- **`--export`** - Analizi dosyaya dışa aktar (JSON/CSV)
- **`--set-duration`** - Playlist analizi için set süresi (dakika)

### DJ Araçları (`dj_tools.py`)

- **`ses_dosyasi`** - Analiz edilecek ses dosyası
- **`--export`** - DJ notlarını dosyaya dışa aktar
- **`--visualize`** - Performans görselleştirmesini göster
- **`--batch`** - Dizini toplu analiz et
- **`--output-dir`** - Toplu analiz için çıktı dizini

## 🔧 Gelişmiş Özellikler

### Ses Analizi (`audio_utils.py`)

```python
from audio_utils import AudioAnalyzer

# Analizörü başlat
analyzer = AudioAnalyzer("parca.mp3")

# Kapsamlı özellikleri al
features = analyzer.get_audio_features()
print(f"BPM: {features['bpm']}")
print(f"Anahtar: {features['key']}")

# Bölümleri tespit et
sections = analyzer.detect_sections()

# Vuruş ızgarasını analiz et
beat_times, beat_strengths = analyzer.analyze_beat_grid()

# Kapsamlı görselleştirme oluştur
analyzer.plot_comprehensive_analysis()
```

### Playlist Yönetimi (`playlist_manager.py`)

```python
from playlist_manager import PlaylistManager

# Playlist yöneticisini başlat
manager = PlaylistManager("/muzik/yolu")

# Playlist'i analiz et
df = manager.analyze_playlist()

# Optimize edilmiş set listesi oluştur
set_list = manager.create_set_list(duration_minutes=60, energy_curve='build')

# Analizi dışa aktar
manager.export_playlist("playlist_analizi.json", format='json')
```

### DJ Performans Araçları (`dj_tools.py`)

```python
from dj_tools import DJTools

# DJ araçlarını başlat
dj_tools = DJTools("parca.mp3")

# Cue noktalarını tespit et
cue_points = dj_tools.detect_cue_points(sensitivity=0.7)

# Döngü önerileri
loops = dj_tools.suggest_loops(min_duration=4.0, max_duration=16.0)

# DJ notları oluştur
notes = dj_tools.generate_dj_notes()

# Performans görselleştirmesi oluştur
dj_tools.create_performance_visualization()
```

## 📈 Analiz Çıktısı

### Parça Bilgileri
- **Süre:** Parça uzunluğu (saniye)
- **BPM:** Güven skoru ile tempo
- **Anahtar:** Güven skoru ile müzikal anahtar
- **Enerji Profili:** Ortalama, maksimum ve standart sapma
- **Bölümler:** Tespit edilen bölüm sayısı ve zamanlaması
- **Drop'lar:** Enerji düşüşü sayısı ve zamanlaması

### Uyumluluk Analizi
- **BPM Uyumluluğu:** Tempo farkına dayalı yüzde
- **Anahtar Uyumluluğu:** Harmonik uyumluluk skoru
- **Enerji Uyumluluğu:** Enerji seviyesi eşleştirmesi
- **Genel Skor:** Tüm faktörlerin ağırlıklı kombinasyonu

### Mix Önerileri
- **Mix Süresi:** Önerilen geçiş uzunluğu
- **Çıkış Noktaları:** Parça 1'den çıkmak için optimal noktalar
- **Giriş Noktaları:** Parça 2'ye girmek için optimal noktalar
- **BPM Senkronizasyonu:** Tempo senkronizasyonu gerekli mi
- **Mix Stratejisi:** Detaylı teknik öneriler

## 🎯 Kullanım Alanları

### DJ Performansı
- **Set Planlama:** Optimal parça sıralamaları oluşturma
- **Cue Noktası Hazırlığı:** En iyi miksaj noktalarını belirleme
- **Harmonik Mixing:** Anahtar uyumluluğunu sağlama
- **Enerji Yönetimi:** Dans pisti enerjisini koruma

### Müzik Prodüksiyonu
- **Referans Analizi:** Referans parçaları analiz etme
- **Yapı Analizi:** Şarkı bölümlerini anlama
- **Enerji Haritalama:** Parça dinamiklerini görselleştirme

### Müzik Keşfi
- **Playlist Optimizasyonu:** Daha iyi playlist'ler oluşturma
- **Uyumluluk Testi:** Parça kombinasyonlarını test etme
- **Tür Analizi:** Müzikal özellikleri anlama

## 🔄 Nasıl Çalışır?

1. **Ses Yükleme:** Her MP3 dosyası Librosa kullanılarak yüklenir ve mono ses sinyaline dönüştürülür.

2. **Özellik Çıkarma:** Birden fazla ses özelliği çıkarılır:
   - RMS enerji seviyeleri
   - Birden fazla algoritma kullanarak BPM tespiti
   - Kromagram aracılığıyla müzikal anahtar analizi
   - Vuruş ızgarası analizi
   - MFCC özellikleri kullanarak bölüm tespiti

3. **Uyumluluk Analizi:** Parçalar birden fazla boyutta karşılaştırılır:
   - BPM farkı ve uyumluluğu
   - Müzik teorisi kullanarak anahtar uyumluluğu
   - Enerji seviyesi eşleştirmesi
   - Genel uyumluluk skorlaması

4. **Mix Noktası Tespiti:** Optimal miksaj noktaları belirlenir:
   - Parça 1'deki enerji vadileri (çıkış noktaları)
   - Parça 2'deki enerji zirveleri (giriş noktaları)
   - Vuruş senkronize noktaları
   - Bölüm sınırları

5. **Görselleştirme:** Kapsamlı grafikler gösterir:
   - Zaman içinde enerji profilleri
   - Vuruş ızgaraları ve zamanlama
   - Anahtar analizi için kromagram
   - Performans bölgeleri ve bölümler

6. **Öneriler:** Detaylı miksaj tavsiyeleri:
   - Önerilen mix süresi
   - Özel zamanlama önerileri
   - Teknik öneriler
   - Potansiyel zorluklar ve çözümler

## 🎨 Özelleştirme

Miksaj tarzınıza uygun şekilde aşağıdaki parametreleri ayarlayabilirsiniz:

### Enerji Analizi
- **`--gecis_suresi`:** Parça 1'in son bölümünde analiz edilecek sürenin uzunluğunu belirleyin
- **`--threshold_factor`:** Parça 2'de enerji artış tespitinin hassasiyetini ayarlayın

### Cue Noktası Tespiti
- **`sensitivity`:** Cue noktası tespit hassasiyetini ayarlayın (0.0-1.0)

### Döngü Önerileri
- **`min_duration`:** Minimum döngü süresi (saniye)
- **`max_duration`:** Maksimum döngü süresi (saniye)

### Playlist Analizi
- **`energy_curve`:** 'build', 'wave', 'peak_middle', 'constant' arasından seçin
- **`key_compatibility`:** Anahtar tabanlı optimizasyonu etkinleştir/devre dışı bırak
- **`bpm_transitions`:** BPM tabanlı optimizasyonu etkinleştir/devre dışı bırak

## 📁 Dosya Yapısı

```
dynamix/
├── mix_analiz.py          # Orijinal temel analiz aracı
├── mix_enhanced.py        # Tüm özelliklerle gelişmiş analiz
├── audio_utils.py         # Temel ses analizi yardımcıları
├── playlist_manager.py    # Playlist ve set listesi yönetimi
├── dj_tools.py           # DJ performans araçları
├── requirements.txt      # Python bağımlılıkları
├── requirements-dev.txt  # Geliştirme bağımlılıkları
├── setup.py             # Paket dağıtım yapılandırması
├── Makefile             # Geliştirme otomasyonu
├── tests/               # Test paketi
│   ├── test_audio_utils.py
│   ├── test_playlist_manager.py
│   ├── test_dj_tools.py
│   └── run_tests.py
├── sample_data/         # Örnek veri dizini
├── docs/               # Dokümantasyon
├── examples.py         # Örnek kullanımlar
├── README.md          # Bu dosya
├── BENIOKU.md         # Türkçe dokümantasyon
└── LICENSE           # MIT Lisansı
```

## 🧪 Test ve Geliştirme

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
make test

# Kapsamlı testler
make test-coverage

# Belirli modül testleri
make test-module MODULE=audio_utils
```

### Kod Kalitesi
```bash
# Kod formatlaması
make format

# Linting kontrolü
make lint

# Güvenlik kontrolü
make security-check
```

### Geliştirme Ortamı
```bash
# Geliştirme kurulumu
make install-dev

# Proje kurulumu
make setup-project

# Sağlık kontrolü
make health-check
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen bir Pull Request gönderin. Büyük değişiklikler için, önce neyi değiştirmek istediğinizi tartışmak üzere bir issue açın.

## 📄 Lisans

Bu proje MIT Lisansı kapsamında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakınız.

## 🙏 Teşekkürler

- [Librosa](https://librosa.org/) - Ses ve müzik sinyal işleme
- [NumPy](https://numpy.org/) - Sayısal hesaplama
- [Matplotlib](https://matplotlib.org/) - Grafik çizimi ve görselleştirme
- [Pandas](https://pandas.pydata.org/) - Veri manipülasyonu ve analizi
- [Seaborn](https://seaborn.pydata.org/) - İstatistiksel veri görselleştirme

---

🎵 **DynaMix ile geçişlerinizde enerjiyi koruyun ve miksajlarınızın akıcılığını artırın!** 🎵
