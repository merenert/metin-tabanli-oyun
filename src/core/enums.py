from enum import Enum,Flag, auto

class OyuncuSlotu(Enum):
    SOL_KOL = auto()
    SAG_KOL = auto()
    GOVDEZIRHI = auto()
    KOLLUK = auto()
    AYAKKABI = auto()

class MapTuru(Flag):
    ORMAN = auto()
    KOY = auto()
    ZINDAN = auto()
    SEHIR = auto()