from dataclasses import dataclass, field
from typing import Self,cast
from core.entity import Entity
from core.enums import OyuncuSlotu
from systems.eventbus import event_bus
from core.datatypes import MapRegion
from systems.components.equipment import EquipmentComponent
from systems.components.stats import StatsComponent
from systems.components.inventory import InventoryComponent
from systems.components.location import LocationComponent
from systems.components.attributes import AttributeComponent
from systems.components.weight import WeightComponent
from core.entity import Entity
# ====class tanımı====

class Karakter(Entity):
    def __init__(self, isim, irk, sinif, dominant_el: OyuncuSlotu):
        super().__init__()
        self.dominant_el = dominant_el
        self.isim = isim
        self.irk = irk
        self.sinif = sinif

    # Artık __post_init__ gerekmez
    def to_dict(self) -> dict:
        return {
            "isim": self.isim,
            "irk": self.irk,
            "sinif": self.sinif,
            "dominant_el": self.dominant_el.name,
            "envanter": (self.al(InventoryComponent).to_dict()),
            "ekipman": (self.al(EquipmentComponent).to_dict()),
            "nitelikler": (self.al(AttributeComponent).to_dict()),
            "stats": (self.al(StatsComponent).to_dict()),
            "konum": (self.al(LocationComponent).to_dict()),
            "agirlik": (self.al(WeightComponent)).to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        isim = data["isim"]
        irk = data["irk"]
        sinif = data["sinif"]
        dominant_el = OyuncuSlotu[data["dominant_el"]]

        karakter = cls(isim, irk, sinif, cast(OyuncuSlotu, dominant_el))

        # Componentleri dict'ten oluşturup ekle
        karakter.ekle(EquipmentComponent.from_dict(karakter, data.get("ekipman", {})))
        karakter.ekle(InventoryComponent.from_dict(karakter, data.get("envanter", {})))
        karakter.ekle(LocationComponent.from_dict(karakter, data.get("konum", {})))
        karakter.ekle(AttributeComponent.from_dict(karakter, data.get("nitelikler", {})))
        karakter.ekle(StatsComponent.from_dict(
            sahip=karakter,
            attribute_component=karakter.al(AttributeComponent),
            data=data.get("stats", {})
        ))
        karakter.ekle(WeightComponent(karakter))
        return karakter
















