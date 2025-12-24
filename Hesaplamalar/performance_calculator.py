"""
VERTİX-H1 Helikopter Performans Hesaplayıcı
============================================

Bu modül, helikopter tasarımı için temel performans hesaplamalarını içerir:
- Güç gereksinimleri (hovering, climb, cruise)
- Menzil ve dayanıklılık hesaplamaları
- Disk yüklemesi ve güç yüklemesi optimizasyonu

Referanslar:
- Prouty, R. W. (2002). Helicopter Performance, Stability, and Control
- Seddon, J., & Newman, S. (2011). Basic Helicopter Aerodynamics
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple

# Sabitler
RHO_SL = 1.225  # kg/m³ - Deniz seviyesi hava yoğunluğu
G = 9.81  # m/s² - Yerçekimi ivmesi
ETA_PROP = 0.85  # Pervane verimi
K_INDUCED = 1.15  # İndüklenmiş güç düzeltme faktörü


class HelicopterPerformance:
    """VERTİX-H1 helikopteri için performans hesaplamaları"""
    
    def __init__(self, mtow: float, rotor_diameter: float, num_blades: int = 5):
        """
        Args:
            mtow: Maksimum kalkış ağırlığı (kg)
            rotor_diameter: Ana rotor çapı (m)
            num_blades: Rotor kanat sayısı
        """
        self.mtow = mtow
        self.rotor_diameter = rotor_diameter
        self.num_blades = num_blades
        self.rotor_area = np.pi * (rotor_diameter / 2) ** 2
        
    def disk_loading(self) -> float:
        """Disk yüklemesi hesapla (N/m²)"""
        weight = self.mtow * G
        return weight / self.rotor_area
    
    def hover_power_ideal(self, altitude: float = 0) -> float:
        """
        İdeal hovering gücü (kW)
        
        Args:
            altitude: İrtifa (m)
        """
        rho = self._air_density(altitude)
        weight = self.mtow * G
        
        # Momentum teorisi: P = T^(3/2) / sqrt(2*rho*A)
        power_ideal = (weight ** 1.5) / np.sqrt(2 * rho * self.rotor_area)
        
        # İndüklenmiş güç düzeltmesi
        power_induced = K_INDUCED * power_ideal
        
        return power_induced / 1000  # W -> kW
    
    def hover_power_total(self, altitude: float = 0) -> float:
        """
        Toplam hovering gücü (profil + indüklenmiş + parazit)
        
        Args:
            altitude: İrtifa (m)
        """
        power_induced = self.hover_power_ideal(altitude)
        
        # Profil gücü (yaklaşık %15-20 indüklenmiş güç)
        power_profile = 0.18 * power_induced
        
        # Parazit gücü (hovering'de minimal)
        power_parasite = 0.05 * power_induced
        
        # Kuyruk rotor gücü (%10-15)
        power_tail = 0.12 * power_induced
        
        return power_induced + power_profile + power_parasite + power_tail
    
    def max_range(self, fuel_capacity: float, sfc: float, cruise_speed: float) -> float:
        """
        Maksimum menzil hesabı (km)
        
        Args:
            fuel_capacity: Yakıt kapasitesi (kg)
            sfc: Özgül yakıt tüketimi (kg/kW/h)
            cruise_speed: Seyir hızı (m/s)
        """
        # Seyir gücü (hovering gücünün ~1.2 katı)
        cruise_power = 1.2 * self.hover_power_total()
        
        # Uçuş süresi
        endurance_hours = fuel_capacity / (sfc * cruise_power)
        
        # Menzil
        range_m = cruise_speed * endurance_hours * 3600
        
        return range_m / 1000  # m -> km
    
    def _air_density(self, altitude: float) -> float:
        """
        İrtifaya göre hava yoğunluğu (ISA standardı)
        
        Args:
            altitude: İrtifa (m)
        """
        # Basitleştirilmiş ISA modeli
        temp_sl = 288.15  # K
        temp_lapse = 0.0065  # K/m
        
        temp = temp_sl - temp_lapse * altitude
        pressure_ratio = (temp / temp_sl) ** 5.256
        
        return RHO_SL * pressure_ratio * (temp_sl / temp)
    
    def plot_power_vs_altitude(self, max_altitude: float = 6000):
        """Güç-İrtifa grafiği çiz"""
        altitudes = np.linspace(0, max_altitude, 50)
        powers = [self.hover_power_total(alt) for alt in altitudes]
        
        plt.figure(figsize=(10, 6))
        plt.plot(altitudes, powers, 'b-', linewidth=2)
        plt.xlabel('İrtifa (m)', fontsize=12)
        plt.ylabel('Hovering Gücü (kW)', fontsize=12)
        plt.title('VERTİX-H1: Hovering Gücü vs İrtifa', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('Analiz/power_vs_altitude.png', dpi=300)
        print("✓ Grafik kaydedildi: Analiz/power_vs_altitude.png")


def main():
    """Ana hesaplama rutini"""
    print("=" * 60)
    print("VERTİX-H1 PERFORMANS ANALİZİ")
    print("=" * 60)
    
    # Helikopter parametreleri
    heli = HelicopterPerformance(
        mtow=1500,  # kg
        rotor_diameter=10.5,  # m
        num_blades=5
    )
    
    print(f"\n📊 TEMEL PARAMETRELER")
    print(f"   MTOW: {heli.mtow} kg")
    print(f"   Rotor Çapı: {heli.rotor_diameter} m")
    print(f"   Rotor Alanı: {heli.rotor_area:.2f} m²")
    print(f"   Disk Yüklemesi: {heli.disk_loading():.2f} N/m²")
    
    print(f"\n⚡ GÜÇ GEREKSİNİMLERİ")
    power_sl = heli.hover_power_total(0)
    power_3000m = heli.hover_power_total(3000)
    power_5500m = heli.hover_power_total(5500)
    
    print(f"   Hovering (Deniz Seviyesi): {power_sl:.2f} kW ({power_sl * 1.341:.2f} shp)")
    print(f"   Hovering (3000m): {power_3000m:.2f} kW ({power_3000m * 1.341:.2f} shp)")
    print(f"   Hovering (5500m): {power_5500m:.2f} kW ({power_5500m * 1.341:.2f} shp)")
    
    print(f"\n🛫 MENZİL VE DAYANIKLILIK")
    fuel_capacity = 350  # kg
    sfc = 0.28  # kg/kW/h (turboşaft tipik değer)
    cruise_speed = 77  # m/s (~150 knots)
    
    max_range = heli.max_range(fuel_capacity, sfc, cruise_speed)
    endurance = fuel_capacity / (sfc * power_sl)
    
    print(f"   Yakıt Kapasitesi: {fuel_capacity} kg")
    print(f"   Seyir Hızı: {cruise_speed} m/s (~{cruise_speed * 1.944:.0f} knots)")
    print(f"   Maksimum Menzil: {max_range:.2f} km")
    print(f"   Dayanıklılık: {endurance:.2f} saat")
    
    print(f"\n📈 Grafik oluşturuluyor...")
    heli.plot_power_vs_altitude()
    
    print("\n" + "=" * 60)
    print("✓ Analiz tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    main()
