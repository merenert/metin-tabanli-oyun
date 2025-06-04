

class Karakter:
    def __init__(self, isim, sinif, can, base_zirh, base_saldiri_gucu, ceviklik):
        self.isim = isim
        self.sinif = sinif
        self.can = can
        self.base_zirh = base_zirh
        self.base_saldiri_gucu = base_saldiri_gucu
        self.envanter = Envanter()
        self.ceviklik = ceviklik
        self.kusanilan = {
            "sol_kol": None,
            "govdezirhi": None,
            "kolluk": None,
            "ayakkabi": None,
            "sag_kol": None,
        }

    def saldiri_gucu(self, silah_turu="sag_kol"):
        bonus = 0
        secili_silah = self.kusanilan.get(silah_turu)
        if secili_silah is not None:
            bonus = secili_silah.hasar_bonusu
        return self.base_saldiri_gucu + bonus

    def zirh(self):
        bonus = 0
        if self.kusanilan["govdezirhi"] is not None:
            bonus += self.kusanilan["govdezirhi"].zirh_bonusu
        if self.kusanilan["kolluk"] is not None:
            bonus += self.kusanilan["kolluk"].zirh_bonusu
        if self.kusanilan["ayakkabi"] is not None:
            bonus += self.kusanilan["ayakkabi"].zirh_bonusu
        return bonus + self.base_zirh

    def esya_kusandir(self, esya):
        if isinstance(esya, Silah):
            self.kusanilan["sag_kol"] = esya
        elif isinstance(esya, Govdezirhi):
            self.kusanilan["govdezirhi"] = esya
        elif isinstance(esya, Kalkan):
            self.kusanilan["sol_kol"] = esya
        elif isinstance(esya, Kolzirhi):
            self.kusanilan["kolluk"] = esya
        elif isinstance(esya, Ayakkabi):
            self.kusanilan["ayakkabi"] = esya
        print(f"{self.isim}, {esya.ekipman} kuşandı.")

    def esya_kusan(self):
        self.envanter.goruntule()
        liste = []
        for ekipman , (a,b) in self.envanter.envanter.items():
            liste.append(a)
        key= input("eklemek istediğiniz eşyayı giriniz:(1/2/3/4/5...)")
        key = int(key)
        key = key -1
        self.esya_kusandir(liste[key])



class Envanter:
    def __init__(self):
        self.envanter = {}

    def ekle(self,ekipman):
        if ekipman in self.envanter:
            self.envanter[ekipman][1]+= 1
        else:
            self.envanter[ekipman] = [ekipman, 1]

    def cikart(self,ekipman):
        if ekipman in self.envanter:
            self.envanter[ekipman][1] -= 1
        if self.envanter[ekipman][1] <= 0:
            self.envanter.pop(ekipman)

    def goruntule(self):
        for ekipman , (a,b) in self.envanter.items():
            print("Envanter:\n" f"- {a.ekipman}: {b} adet")








# === Ekipman sınıfları ===

class Ekipman:
    def __init__(self, ekipman):
        self.ekipman = ekipman

class Silah(Ekipman):
    def __init__(self, ekipman, hasar_bonusu):
        super().__init__(ekipman)
        self.hasar_bonusu = hasar_bonusu

class Govdezirhi(Ekipman):
    def __init__(self, ekipman, zirh_bonusu):
        super().__init__(ekipman)
        self.zirh_bonusu = zirh_bonusu

class Kolzirhi(Ekipman):
    def __init__(self, ekipman, zirh_bonusu):
        super().__init__(ekipman)
        self.zirh_bonusu = zirh_bonusu

class Ayakkabi(Ekipman):
    def __init__(self, ekipman, zirh_bonusu):
        super().__init__(ekipman)
        self.zirh_bonusu = zirh_bonusu

class Kalkan(Ekipman):
    def __init__(self, ekipman, zirh_bonusu, hasar_bonusu):
        super().__init__(ekipman)
        self.zirh_bonusu = zirh_bonusu
        self.hasar_bonusu = hasar_bonusu

# === Ekipman örnekleri ===

Uzun_kilic = Silah("Uzun Kılıç", hasar_bonusu=5)
demir_zirh = Govdezirhi("Demir Zırh", zirh_bonusu=10)
deri_kolluk = Kolzirhi("Deri Kolluk", zirh_bonusu=5)
deri_ayakkabi = Ayakkabi("Deri Ayakkabı", zirh_bonusu=3)
post_kalkan = Kalkan("Post Kalkan", zirh_bonusu=5, hasar_bonusu=3)

# === Karakter sınıfları ===

KARAKTER_SINIFLARI = {
    "okçu": {
        "can": 80,
        "base_zirh": 15,
        "base_saldiri_gucu": 30,
        "ceviklik": 2,
    },
    "savasci": {
        "can": 100,
        "base_zirh": 20,
        "base_saldiri_gucu": 15,
        "ceviklik": 3,
    }
}

# === Karakter oluşturma fonksiyonu ===

def karakter_olustur():
    isim = input("Karakter ismini gir: ")

    print("Sınıf seçimi:")
    siniflar = list(KARAKTER_SINIFLARI.keys())
    for i, sinif_adi in enumerate(siniflar, 1):
        print(f"{i}. {sinif_adi.capitalize()}")

    while True:
        secim = input("Seçiminiz (1/2): ")
        if secim in ["1", "2"]:
            secilen_sinif = siniflar[int(secim) - 1]
            break
        else:
            print("Geçerli bir sayı girin (1 veya 2).")

    statlar = KARAKTER_SINIFLARI[secilen_sinif]

    karakter = Karakter(
        isim=isim,
        sinif=secilen_sinif,
        can=statlar["can"],
        base_zirh=statlar["base_zirh"],
        base_saldiri_gucu=statlar["base_saldiri_gucu"],
        ceviklik=statlar["ceviklik"]
    )
    return karakter

# === Karakter oluşturuluyor ===

oyuncu = karakter_olustur()
print(f"{oyuncu.isim} ({oyuncu.sinif}) sınıfından.")
oyuncu.envanter.ekle(Uzun_kilic)
oyuncu.envanter.ekle(demir_zirh)
oyuncu.envanter.ekle(deri_ayakkabi)
oyuncu.envanter.ekle(post_kalkan)
oyuncu.envanter.ekle(deri_kolluk)


