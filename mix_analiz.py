import librosa
import numpy as np
import matplotlib.pyplot as plt
import argparse

def analiz_yukle(dosya_yolu, hop_length=512):
    """
    Belirtilen MP3 dosyasını yükler, RMS enerji değerlerini hesaplar
    ve zaman dizisini oluşturur.
    """
    # librosa.load varsayılan olarak mono yükleme yapar.
    y, sr = librosa.load(dosya_yolu, sr=None)  
    # RMS enerji hesaplama (hop_length ile parçalar halinde)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    # RMS hesaplaması yapılan her frame için zaman bilgisi
    zamanlar = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
    return y, sr, rms, zamanlar

def enerji_artis_zamani(rms, zamanlar, threshold_factor=1.2):
    """
    Parçanın başından itibaren, ilk birkaç frame’ın ortalamasını baz (baseline) alıp,
    RMS değeri bu baz değerin threshold_factor katını aşan ilk zamanı bulur.
    """
    # İlk 10 frame’ı baz olarak alalım (bu değeri ihtiyaca göre ayarlayabilirsiniz)
    baz_deger = np.mean(rms[:10])
    
    for i, deger in enumerate(rms):
        if deger > baz_deger * threshold_factor:
            return zamanlar[i]
    return None

def gecis_analizi(parca1_dosyasi, parca2_dosyasi, gecis_suresi=10, threshold_factor=1.2):
    """
    İki parçayı analiz edip, parça1'in son kısmı ile parça2'nin giriş kısmındaki
    enerji farkına dair önerilerde bulunur.
    
    - parca1_dosyasi: İlk parçanın MP3 dosya yolu.
    - parca2_dosyasi: İkinci parçanın MP3 dosya yolu.
    - gecis_suresi: Parça1'in son kaç saniyelik bölümünün analiz edileceği.
    - threshold_factor: Parça2’nin başlangıç enerji artışının tespitinde kullanılacak eşik çarpanı.
    """
    # Parça 1 analiz
    y1, sr1, rms1, zamanlar1 = analiz_yukle(parca1_dosyasi)
    parca1_suresi = zamanlar1[-1]
    # Parça1'in son "gecis_suresi" saniyesini alalım
    mask = zamanlar1 >= (parca1_suresi - gecis_suresi)
    parca1_son_enerji = np.mean(rms1[mask])
    
    # Parça 2 analiz
    y2, sr2, rms2, zamanlar2 = analiz_yukle(parca2_dosyasi)
    # Parça2'nin başından itibaren enerji artış noktasını tespit edelim
    artis_zaman = enerji_artis_zamani(rms2, zamanlar2, threshold_factor=threshold_factor)
    
    # Sonuç ve önerileri yazdır
    print("=== Analiz Sonuçları ===")
    print(f"Parça 1 süresi: {parca1_suresi:.2f} saniye")
    print(f"Parça 1'in son {gecis_suresi} saniyesinin ortalama enerji değeri: {parca1_son_enerji:.5f}")
    if artis_zaman is not None:
        print(f"Parça 2'de enerji artış noktası yaklaşık {artis_zaman:.2f} saniyede tespit edildi.")
    else:
        print("Parça 2'de enerji artış noktası tespit edilemedi. Lütfen parçayı manuel kontrol ediniz.")
    
    print("\nÖneri:")
    if artis_zaman is not None:
        print(f"- Parça 2, {artis_zaman:.2f} saniyeye kadar daha düşük enerjiye sahip. "
              "Bu durumda, parça 1'in son {0} saniyelik bölümünü, parça 2'nin enerjik giriş noktasına kadar "
              "karıştırmayı (mix) deneyebilirsiniz.".format(gecis_suresi))
    else:
        print("- Enerji artış noktası tespit edilemediği için geçiş süresini manuel olarak ayarlamanız önerilir.")
    
    # Opsiyonel: Enerji eğrilerini görselleştirelim
    plt.figure(figsize=(12, 6))
    
    # Parça 1 grafiği
    plt.subplot(2, 1, 1)
    plt.plot(zamanlar1, rms1, label="Parça 1 RMS Enerji")
    plt.axvline(x=parca1_suresi - gecis_suresi, color='r', linestyle='--', label="Geçiş Başlangıcı")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("RMS Enerji")
    plt.title("Parça 1 Enerji Eğrisi")
    plt.legend()
    
    # Parça 2 grafiği
    plt.subplot(2, 1, 2)
    plt.plot(zamanlar2, rms2, label="Parça 2 RMS Enerji")
    if artis_zaman is not None:
        plt.axvline(x=artis_zaman, color='g', linestyle='--', label="Enerji Artış Noktası")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("RMS Enerji")
    plt.title("Parça 2 Enerji Eğrisi")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="İki MP3 dosyasını analiz ederek, geçişte dinleyici enerjisinin korunması için öneriler sunar."
    )
    parser.add_argument("parca1", type=str, help="İlk MP3 dosyasının yolu (ör. Tarkan'ın 'Öp')")
    parser.add_argument("parca2", type=str, help="İkinci MP3 dosyasının yolu (ör. Ajda Pekkan'ın 'Harika')")
    parser.add_argument("--gecis_suresi", type=float, default=10,
                        help="Parça1'in son kaç saniyesinin analiz edileceği (varsayılan: 10 saniye)")
    parser.add_argument("--threshold_factor", type=float, default=1.2,
                        help="Enerji artış tespitinde kullanılacak eşik çarpanı (varsayılan: 1.2)")
    
    args = parser.parse_args()
    
    gecis_analizi(args.parca1, args.parca2, gecis_suresi=args.gecis_suresi, threshold_factor=args.threshold_factor)
