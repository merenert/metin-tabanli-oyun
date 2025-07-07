from dataclasses import dataclass, field
from typing import Dict, Optional , Self
from core.enums import OyuncuSlotu
from core.inventory import Envanter
from core.datatypes import ItemProto
@dataclass(slots=True)
class Karakter:
    isim: str
    sinif: str
    can: int
    irk: str
    base_zirh: int
    base_saldiri_gucu: int
    ceviklik: int
    dominant_el: OyuncuSlotu
    envanter: Envanter = field(default_factory=Envanter)
    kusanilan: Dict[OyuncuSlotu, Optional[ItemProto]] = field(init=False)

    def __post_init__(self):
        self.kusanilan = {slot: None for slot in OyuncuSlotu}

    @property
    def zirh(self):
        return self.base_zirh + sum(p.zirh_bonusu for p in self.kusanilan.values() if p)

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
        if self.kusanilan[s] is not None:
            raise ValueError(f"{s.name} slotu dolu")

    return proto, actual_slots


def kusan(self, item_id: str, slot: OyuncuSlotu | None = None):
    proto, actual_slots = self.kusanma_kontrolu(item_id, slot)

    for s in actual_slots:
        self.kusanilan[s] = proto

    self.envanter.cikart(item_id, 1)