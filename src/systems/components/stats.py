from typing import Protocol,cast
from core.enums import OyuncuSlotu

class StatsComponent:
    def __init__(self,
                 sahip,
                 can: int,
                 base_zirh: int,
                 base_saldiri_gucu: int,
                 base_ceviklik: int,
                 dominant_el: OyuncuSlotu
                 ):
        self.sahip = sahip
        self.can = can
        self.base_zirh = base_zirh
        self.base_saldiri_gucu = base_saldiri_gucu
        self.base_ceviklik = base_ceviklik
        self.dominant_el = dominant_el

    @property
    def zirh(self):
        return self.base_zirh + sum(
            p.zirh_bonusu for p in self.sahip.ekipman.kusanilan.values() if p
        )

    def saldiri_gucu(self, el: OyuncuSlotu = None) -> int:
        el = el or self.dominant_el
        item: ItemProto | None = self.sahip.ekipman.kusanilan.get(el)
        if item is None:
            return self.base_saldiri_gucu
        return self.base_saldiri_gucu + item.hasar_bonusu

    @property
    def ceviklik(self):
        return self.base_ceviklik + sum(
            p.ceviklik_bonusu for p in self.sahip.ekipman.kusanilan.values() if p
        )


    def to_dict(self) -> dict:
        return {
            "can": self.can,
            "base_zirh": self.base_zirh,
            "base_saldiri_gucu": self.base_saldiri_gucu,
            "base_ceviklik": self.base_ceviklik,
            "dominant_el": self.dominant_el.name
        }

    @classmethod
    def from_dict(cls, sahip, data: dict):
        return cls(
            sahip=sahip,
            can=data.get("can", 100),
            base_zirh=data.get("base_zirh", 0),
            base_saldiri_gucu=data.get("base_saldiri_gucu", 10),
            base_ceviklik=data.get("base_ceviklik", 5),
            dominant_el = cast(OyuncuSlotu, OyuncuSlotu[data["dominant_el"]])
        )