from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Optional

class Slot(Enum):
    SOL_KOL = auto()
    SAG_KOL = auto()
    GOVDEZIRHI = auto()
    KOLLUK = auto()
    AYAKKABI = auto()

@dataclass(frozen=True, slots=True)
class RaceProto:
    id: str
    can: int
    base_zirh: int
    base_saldiri_gucu: int
    ceviklik: int
    dominant_el: Slot

@dataclass(frozen=True, slots=True)
class ClassProto:
    id: str
    can: int
    base_saldiri_gucu: int
    ceviklik: int

#Ekipman sınıfı
@dataclass(frozen=True, slots=True)
class ItemProto:
    id: str
    name: str
    slots: tuple[Slot,...]
    cift_el_kullan: bool = False
    zirh_bonusu: int = 0
    hasar_bonusu: int = 0
    engelleme: int = 0
# === Envanter İşlemleri ===

class Envanter:
    def __init__(self):
        self.inventory: dict[str,int]= {}

    def ekle(self, item_id: str, adet: int = 1):
        if adet <= 0:
            raise ValueError("adet pozitif olmalı")
        self.inventory[item_id] = self.inventory.get(item_id, 0) + adet

    def cikart(self,item_id: str, adet: int = 1):
        if adet <= 0:
            raise ValueError("adet pozitif bir sayı olmalı")
        try:
            mevcut = self.inventory[item_id]
        except KeyError:
            raise ValueError("item envanterde yok")
        if adet > mevcut:
            raise ValueError(f"Envantede yalnızca {mevcut} adet var; {adet} çıkarılamaz")
        kalan = mevcut - adet
        if kalan:
            self.inventory[item_id] = kalan
        else:
            self.inventory.pop(item_id)
    def miktar(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)

    def list_idleri(self) -> list[str]:
        return list(self.inventory.keys())
#== Karakter Oluşturma ve Envanter fonksiyonları ==
@dataclass(slots=True)
class Karakter:
    isim: str
    sinif: str
    can: int
    irk: str
    base_zirh: int
    base_saldiri_gucu: int
    ceviklik: int
    dominant_el: Slot
    envanter: Envanter = field(default_factory=Envanter)
    kusanilan: Dict[Slot, Optional[ItemProto]] = field(init=False)

    def __post_init__(self):
        self.kusanilan = {slot: None for slot in Slot}

    @classmethod
    def karakterolustur(cls, name: str, race_id: str, class_id: str,
               hand: Slot | None = None)-> Karakter :
        race = IRKLAR[race_id]
        klass = SINIFLAR[class_id]
        dom = hand or race.dominant_el

        return cls(
            isim=name,
            irk=race_id,
            sinif=class_id,
            can=race.can + klass.can,
            base_zirh=race.base_zirh,
            base_saldiri_gucu=race.base_saldiri_gucu + klass.base_saldiri_gucu,
            ceviklik=race.ceviklik + klass.ceviklik,
            dominant_el=dom,
        )

    def zirh(self):
        bonus = sum(p.zirh_bonusu for p in self.kusanilan.values() if p)
        return bonus + self.base_zirh

    def kusan(self, item_id:str, slot: Slot | None = None):
        try:
            proto = ITEMS[item_id]
        except KeyError:
            raise ValueError(f"Geçersiz item id: {item_id}") from None
        if self.envanter.miktar(item_id) < 1: ##
            raise ValueError("Envanterde bu eşyadan yok")

            # 2) Parametre uyumu
        if len(proto.slots) > 1 and proto.cift_el_kullan and slot is not None:
            raise ValueError("eşya iki el isteğinden slot seçilemez")
        if slot is not None and slot not in proto.slots:
            raise ValueError("Bu item belirtilen slota takılamaz")

            # 3) Hangi slot(lar)?
        if len(proto.slots) > 1 and proto.cift_el_kullan:
            actual_slots = proto.slots  # tüm mecburi slotlar
        else:
            chosen = slot or self.dominant_el  # verilen ya da dominant
            if chosen not in proto.slots:
                raise ValueError("Dominant el bu eşyayla uyuşmuyor")
            actual_slots = (chosen,)

            # 4) Doluluk kontrolü
        for s in actual_slots:
            if self.kusanilan[s] is not None:
                raise ValueError(f"{s.name} slotu dolu")

            # 5) Kuşan & stok düş
        for s in actual_slots:
            self.kusanilan[s] = proto
        self.envanter.cikart(item_id, 1)

# === Ekipman örnekleri ===
ITEMS: dict[str, ItemProto] = {
    "iron_sword": ItemProto("iron_sword", "Iron Sword", (Slot.SAG_KOL, Slot.SOL_KOL), hasar_bonusu=5,engelleme=1),
    "wood_shield": ItemProto("wood_shield", "Wooden Shield", (Slot.SOL_KOL,Slot.SAG_KOL), zirh_bonusu=2,engelleme=3),
    "leather_boots": ItemProto("leather_boots", "Leather Boots", (Slot.AYAKKABI,), zirh_bonusu=3),
    "leather_suit": ItemProto("leather_suit", "Leather Suit", (Slot.GOVDEZIRHI,), zirh_bonusu=15),
    "leather_arm_floats": ItemProto("leather_arm_floats", "Leather Arm FLoats", (Slot.KOLLUK,), zirh_bonusu=8)
}

# === Karakter sınıfları örnekleri ===

SINIFLAR: dict[str, ClassProto] = {
    "okcu":  ClassProto("okcu", 0, 20, 2),
    "savasci": ClassProto("savasci", 10, 15, 3),
}

# === Irk örnekleri ===
IRKLAR: dict[str, RaceProto] = {
    "elf": RaceProto("elf", 80, 0, 20, 2, Slot.SOL_KOL),
    "ork": RaceProto("ork", 130, 5, 15, -1, Slot.SAG_KOL),
}


