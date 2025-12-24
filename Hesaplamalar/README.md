# VERTİX-H1 Hesaplama Modülleri

Bu klasör, helikopter tasarımı için gerekli mühendislik hesaplamalarını içeren Python betiklerini barındırır.

## 📁 İçerik

### `performance_calculator.py`
Helikopter performans hesaplamaları:
- **Disk Yüklemesi** – Rotor disk alanı başına düşen ağırlık
- **Hovering Gücü** – İrtifaya bağlı güç gereksinimleri
- **Menzil & Dayanıklılık** – Yakıt tüketimine dayalı hesaplamalar
- **Güç-İrtifa Grafiği** – Performans görselleştirmesi

## 🚀 Kullanım

```bash
# Gerekli kütüphaneleri yükle
pip install numpy matplotlib

# Hesaplamaları çalıştır
python performance_calculator.py
```

## 📊 Çıktılar

- Konsol çıktısı: Temel parametreler, güç gereksinimleri, menzil/dayanıklılık
- Grafik: `Analiz/power_vs_altitude.png`

## 📚 Referanslar

- Prouty, R. W. (2002). *Helicopter Performance, Stability, and Control*
- Seddon, J., & Newman, S. (2011). *Basic Helicopter Aerodynamics*
