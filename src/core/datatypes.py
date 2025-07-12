from dataclasses import dataclass, field
from core.enums import OyuncuSlotu
@dataclass(frozen=True, slots=True)
class RaceProto:
    race_id: str
    can: int
    base_zirh: int
    base_saldiri_gucu: int
    base_ceviklik: int
    dominant_el: OyuncuSlotu

@dataclass(frozen=True, slots=True)
class ClassProto:
    class_id: str
    can: int
    base_saldiri_gucu: int
    base_ceviklik: int
    base_zirh: int

#Ekipman sınıfı
@dataclass(frozen=True, slots=True)
class ItemProto:
    item_id: str
    name: str
    slots: tuple[OyuncuSlotu,...]
    cift_el_kullan: bool = False
    zirh_bonusu: int = 0
    hasar_bonusu: int = 0
    engelleme: int = 0
    ceviklik_bonusu: int = 0

@dataclass(frozen=True)
class MapRegion:
    region_id: str
    name: str
    komsular:list[str]
    npc_idleri:list[str]