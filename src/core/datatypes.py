from dataclasses import dataclass, field
from core.enums import OyuncuSlotu
@dataclass(frozen=True, slots=True)
class RaceProto:
    id: str
    can: int
    base_zirh: int
    base_saldiri_gucu: int
    ceviklik: int
    dominant_el: OyuncuSlotu

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
    slots: tuple[OyuncuSlotu,...]
    cift_el_kullan: bool = False
    zirh_bonusu: int = 0
    hasar_bonusu: int = 0
    engelleme: int = 0