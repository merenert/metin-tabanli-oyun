from dataclasses import dataclass, field
from core.enums import OyuncuSlotu, MapTuru


@dataclass(frozen=True, slots=True)
class RaceProto:
    race_id: str
    guc: float
    zeka: float
    hiz: float
    dayaniklilik: float
    dominant_el: OyuncuSlotu

@dataclass(frozen=True, slots=True)
class ClassProto:
    class_id: str
    guc: float = 0.0
    zeka: float = 0.0
    hiz: float = 0.0
    dayaniklilik: float = 0.0

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
    agirlik: float = 0.0

@dataclass(frozen=True)
class MapRegion:
    region_id: str
    name: str
    komsular:list[str]
    npc_idleri:list[str]
    map_turu: MapTuru