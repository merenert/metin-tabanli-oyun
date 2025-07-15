from dataclasses import dataclass, field
from typing import Self
from core.enums import OyuncuSlotu
from systems.eventbus import event_bus
from core.datatypes import MapRegion
from systems.components.equipment import EquipmentComponent
from systems.components.stats import StatsComponent
from systems.components.inventory import InventoryComponent
from systems.components.location import LocationComponent
# ====class tanımı====
@dataclass(slots=True)
class Karakter:
    isim: str
    irk: str
    sinif: str

    stats: StatsComponent = field(init=False)
    ekipman: EquipmentComponent = field(init=False)
    envanter: InventoryComponent = field(init=False)
    konum: LocationComponent = field(init=False)


    # Artık __post_init__ gerekmez
    def to_dict(self) -> dict:
        return {
            "isim": self.isim,
            "irk": self.irk,
            "sinif": self.sinif,
            "stats": self.stats.to_dict(),
            "ekipman": self.ekipman.to_dict(),
            "envanter": self.envanter.to_dict(),
            "konum": self.konum.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        isim = data["isim"]
        irk = data["irk"]
        sinif = data["sinif"]

        # stats içinden dominant_el çekilecek
        dominant_el = OyuncuSlotu[data["stats"]["dominant_el"]]

        # nesneyi oluştur (bileşensiz)
        karakter = cls(isim, irk, sinif,)

        # bileşenleri sırayla kur
        karakter.stats = StatsComponent.from_dict(karakter, data["stats"])
        karakter.ekipman = EquipmentComponent.from_dict(karakter, data["ekipman"])
        karakter.envanter = InventoryComponent.from_dict(karakter, data.get("envanter", {}))
        karakter.konum = LocationComponent.from_dict(karakter, data.get("konum", {}))

        return karakter
















