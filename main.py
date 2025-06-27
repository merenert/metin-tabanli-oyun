from enum import Enum, auto, IntEnum

class Slot(Enum):
    SOL_KOL = auto()
    SAG_KOL = auto()
    GOVDEZIRHI = auto()
    KOLLUK = auto()
    AYAKKABI = auto()

class El(IntEnum):
    SAG = auto()
    SOL = auto()

class Karakter:
    def __init__(self, isim, sinif, can,irk, base_zirh, base_saldiri_gucu, ceviklik,baskin_el):
        self.isim = isim
        self.sinif = sinif
        self.can = can
        self.base_zirh = base_zirh
        self.base_saldiri_gucu = base_saldiri_gucu
        self.envanter = Envanter()
        self.irk = irk
        self.baskin_el = baskin_el
        self.ceviklik = ceviklik
        self.kusanilan = {slot: None for slot in Slot}

    def zirh(self):
        bonus = 0
        if self.kusanilan[Slot.GOVDEZIRHI] is not None:
            bonus += self.kusanilan[Slot.GOVDEZIRHI].zirh_bonusu
        if self.kusanilan[Slot.KOLLUK] is not None:
            bonus += self.kusanilan[Slot.KOLLUK].zirh_bonusu
        if self.kusanilan[Slot.AYAKKABI] is not None:
            bonus += self.kusanilan[Slot.AYAKKABI].zirh_bonusu
        return bonus + self.base_zirh

    def esya_kusandir(self, esya: "Ekipman", slot: Slot | None = None):
        if isinstance(esya, Silah):
            slot = slot or self.baskin_el
            if slot not in (Slot.SAG_KOL, Slot.SOL_KOL):
                raise ValueError("Silah yalnızca SAG_KOL veya SOL_KOL slotuna kuşanabilir.")
            self.kusanilan[slot] = esya
        elif isinstance(esya, Govdezirhi):
            self.kusanilan[Slot.GOVDEZIRHI] = esya
        elif isinstance(esya, Kolzirhi):
            self.kusanilan[Slot.KOLLUK] = esya
        elif isinstance(esya, Ayakkabi):
            self.kusanilan[Slot.AYAKKABI] = esya
        print(f"{self.isim}, {esya.ekipman} kuşandı.")

    def esya_kusan(self, index: int, slot: Slot | None = None): #esya kusandır kullanarak esya kusanmayı sağlayan fonksiyon
        liste = [kayit[0] for kayit in self.envanter.envanter.values()]
        if not (0 <= index < len(liste)):
            raise IndexError("Geçersiz eşya indeksi.")
        self.esya_kusandir(liste[index], slot=slot)

# === Envanter İşlemleri ===

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
    def __init__(self, ekipman, hasar_bonusu,engelleme):
        super().__init__(ekipman)
        self.hasar_bonusu = hasar_bonusu
        self.engelleme = engelleme

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


# === Ekipman örnekleri ===

Uzun_kilic = Silah("Uzun Kılıç",engelleme=0, hasar_bonusu=5)
demir_zirh = Govdezirhi("Demir Zırh", zirh_bonusu=10)
deri_kolluk = Kolzirhi("Deri Kolluk", zirh_bonusu=5)
deri_ayakkabi = Ayakkabi("Deri Ayakkabı", zirh_bonusu=3)
post_kalkan = Silah("Post Kalkan", engelleme=5, hasar_bonusu=3)

# === Karakter sınıfları örnekleri ===

KARAKTER_SINIFLARI = {
    "okçu": {
        "can": 0,
        "base_saldiri_gucu": 20,
        "ceviklik": 2,
    },
    "savasci": {
        "can": 10,
        "base_saldiri_gucu": 15,
        "ceviklik": 3,
    }
}

# === Irk örnekleri ===
IRKLAR = {
    "elf": {
        "can": 80,
        "base_zirh": 0,
        "base_saldiri_gucu": 20,
        "ceviklik": 2,
        "aciklama": "Hafif yapılı, çevik, menzilli savaşta ustalaşmış."
    },
    "ork": {
        "can": 130,
        "base_zirh": 5,
        "base_saldiri_gucu": 15,
        "ceviklik": -1,
        "aciklama": "Güçlü ama hantal. Yakın dövüşte avantajlı."
    },
    "cuce": {
        "can": 150,
        "base_zirh": 3,
        "base_saldiri_gucu": 20,
        "ceviklik": -1,
        "aciklama": "Dayanıklı ve zırhlı, ama daha yavaş."
    },
    "insan": {
        "can": 100,
        "base_zirh": 0,
        "base_saldiri_gucu": 18,
        "ceviklik": 1,
        "aciklama": "Her şeyden biraz, özel bir avantajı yok."
    },
}




# === Karakter oluşturma fonksiyonu ===
def karakter_olustur(isim:str, el:El, secilen_irk:int, secilen_sinif:int):
    if el not in ["sag", "sol"]:
        raise ValueError("Baskın el ya 'sag' ya da 'sol' olmalı.")
    if secilen_irk not in IRKLAR:
        raise ValueError("Geçersiz ırk seçimi.")
    if secilen_sinif not in KARAKTER_SINIFLARI:
        raise ValueError("Geçersiz sınıf seçimi.")

    irk_statlar = IRKLAR[secilen_irk]
    statlar = KARAKTER_SINIFLARI[secilen_sinif]

    karakter = Karakter(
        isim=isim,
        irk=secilen_irk,
        sinif=secilen_sinif,
        can=statlar["can"] + irk_statlar["can"],
        base_zirh=irk_statlar["base_zirh"],
        base_saldiri_gucu=statlar["base_saldiri_gucu"] + irk_statlar["base_saldiri_gucu"],
        ceviklik=statlar["ceviklik"] + irk_statlar["ceviklik"],
        baskin_el=el
    )
    return karakter


