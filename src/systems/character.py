from dataclasses import dataclass, field
from typing import Dict, Optional , Self
from core.enums import OyuncuSlotu
from core.inventory import Envanter
from systems.eventbus import event_bus
from core.datatypes import ItemProto,MapRegion
from veriler import veriyukleyici
from systems.character_factory import Karakterolusturucu
from systems.combat import CombatSystem
from veriler.data_repo import ITEMS


#====class tanımı====
@dataclass(slots=True)
class Karakter:
    isim: str
    sinif: str
    can: int
    irk: str
    base_zirh: int
    base_saldiri_gucu: int
    base_ceviklik: int
    dominant_el: OyuncuSlotu
    bulundugu_bolge: str
    envanter: Envanter = field(default_factory=Envanter)
    kusanilan: Dict[OyuncuSlotu, Optional[ItemProto]] = field(init=False)
    combat_system: CombatSystem = field(init=False)

    def __post_init__(self):
        self.kusanilan = {slot: None for slot in OyuncuSlotu}
        self.combat_system = CombatSystem()

    #====savaş içi kullanılabilir statlar====
    @property
    def zirh(self):
        return self.base_zirh + sum(p.zirh_bonusu for p in self.kusanilan.values() if p)
    def saldiri_gucu(self, el: OyuncuSlotu = None) -> int:
        if el is None:
            el = self.dominant_el
        item = self.kusanilan.get(el)
        if item is None:
            return self.base_saldiri_gucu
        return self.base_saldiri_gucu + item.hasar_bonusu
    @property
    def ceviklik(self):
        return self.base_ceviklik + sum(p.ceviklik_bonusu for p in self.kusanilan.values() if p)

    def saldir(self, hedef, el):
        return self.combat_system.saldir(self, hedef, el)

    # ====kaydetme için verileri sözlüğe çevirme ve sözlükten tekrar eski haline getirme====
    def to_dict(self) -> dict:
        return {
            "isim": self.isim,
            "irk": self.irk,
            "sinif": self.sinif,
            "can": self.can,
            "envanter": self.envanter.inventory,
            "bulundugu_bolge": self.bulundugu_bolge,
            "kusanilan": {
                s: item.item_id
                for s, item in self.kusanilan.items()
                if item is not None
            }
        }
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        isim = data["isim"]
        irk = data["irk"]
        sinif = data["sinif"]
        bulundugu_bolge = data.get("bulundugu_bolge","orman_koyu")

        karakter = Karakterolusturucu.karakterolustur(isim, irk, sinif,bulundugu_bolge)

        karakter.can = data["can"]
        karakter.envanter.inventory = data["envanter"]
        karakter.envanter.sahip = karakter

        karakter.kusanilan = {
            slot: ITEMS[item_id]
            for slot, item_id in data["kusanilan"].items()
        }
        return karakter


#====envanterden eşya kuşanma====
    def kusanma_kontrolu(self, item_id: str, slot: OyuncuSlotu | None = None) -> tuple[ItemProto, tuple[OyuncuSlotu, ...]]:
        try:
            proto = ITEMS[item_id]
        except KeyError:
            raise ValueError(f"Geçersiz item id: {item_id}") from None

        if self.envanter.miktar(item_id) < 1:
            raise ValueError("Envanterde bu eşyadan yok")

        if len(proto.slots) > 1 and proto.cift_el_kullan and slot is not None:
            raise ValueError("Eşya çift el kullanıyor; slot seçilemez")

        if slot is not None and slot not in proto.slots:
            raise ValueError("Bu item belirtilen slota takılamaz")

        # Slot belirleme
        if len(proto.slots) > 1 and proto.cift_el_kullan:
            actual_slots = proto.slots
        else:
            chosen = slot or self.dominant_el
            if chosen not in proto.slots:
                raise ValueError("Dominant el bu eşyayla uyuşmuyor")
            actual_slots = (chosen,)

        # Doluluk kontrolü
        for s in actual_slots:
            if self.kusanilan.get(s) is not None:
                raise ValueError(f"{s.name} slotu dolu")

        return proto, actual_slots
    def kusan(self, item_id: str, slot: OyuncuSlotu | None = None):
        proto, actual_slots = self.kusanma_kontrolu(item_id, slot)

        for s in actual_slots:
            self.kusanilan[s] = proto
            event_bus.publish("esya_kusandi", {
                "karakter": self,
                "item_id": proto,
                "el": s
            })
        self.envanter.cikart(item_id, 1)

    def bolge_degistir(self, yeni_bolge: str, regions: dict[str, MapRegion]) -> bool:
        mevcut = regions[self.bulundugu_bolge]
        if yeni_bolge not in mevcut.komsular:
            return False

        onceki = self.bulundugu_bolge
        self.bulundugu_bolge = yeni_bolge

        event_bus.publish("bolge_degisti", {
            "karakter": self,
            "onceki": onceki,
            "yeni": yeni_bolge
        })

        return True














    