from dataclasses import dataclass
from core.entity import Entity
from typing import cast
from core.enums import OyuncuSlotu
from systems.components.attributes import AttributeComponent
from systems.components.equipment import EquipmentComponent
from core.datatypes import ItemProto


@dataclass
class StatsComponent:
    sahip: Entity  # ✅ 1. sahibin en başta olması daha doğru
    attribute_component: AttributeComponent

    can: float = 0
    base_zirh: float = 0
    base_saldiri_gucu: float = 0
    base_ceviklik: float = 0
    base_tasima_limiti: float = 0

    def __post_init__(self):
        self.calculate_stats()

    def update(self):
        """Nitelikler değiştiğinde yeniden hesaplamak için"""
        self.calculate_stats()

    @property
    def zirh(self) -> float:
        ekipman = self.sahip.al(EquipmentComponent)
        return self.base_zirh + sum(
            p.zirh_bonusu for p in ekipman.kusanilan.values() if p
        )

    def saldiri_gucu(self, el: OyuncuSlotu = None) -> float:
        el = el or self.sahip.dominant_el
        ekipman = self.sahip.al(EquipmentComponent)
        item: ItemProto | None = ekipman.kusanilan.get(el)
        if item is None:
            return self.base_saldiri_gucu
        return self.base_saldiri_gucu + item.hasar_bonusu

    @property
    def ceviklik(self) -> float:
        ekipman = self.sahip.al(EquipmentComponent)
        return self.base_ceviklik + sum(
            p.ceviklik_bonusu for p in ekipman.kusanilan.values() if p
        )
    def tasima_limiti(self) -> float:
        return self.sahip.al(WeightComponent).kalan_limit

    def to_dict(self) -> dict:
        return {
            "can": self.can,
            "base_zirh": self.base_zirh,
            "base_saldiri_gucu": self.base_saldiri_gucu,
            "base_ceviklik": self.base_ceviklik,
            "base_tasima_limiti": self.base_tasima_limiti,
            "zirh": self.zirh,
            "ceviklik": self.ceviklik,
            "saldiri_gucu": self.saldiri_gucu(),
        }

    @classmethod
    def from_dict(cls, sahip: Entity, attribute_component: AttributeComponent, data: dict):
        obj = cls(
            sahip=sahip,
            attribute_component=attribute_component,
        )
        obj.can = data.get("can", 0)
        obj.base_zirh = data.get("base_zirh", 0)
        obj.base_saldiri_gucu = data.get("base_saldiri_gucu", 0)
        obj.base_ceviklik = data.get("base_ceviklik", 0)
        obj.base_tasima_limiti = data.get("base_tasima_limiti", 0)

        obj.calculate_stats()
        return obj

    def calculate_stats(self):
        """AttributeComponent değerlerine göre temel statları hesaplar"""
        self.can = self.attribute_component.dayaniklilik * 20
        self.base_zirh = self.attribute_component.dayaniklilik * 1.5
        self.base_saldiri_gucu = self.attribute_component.guc * 3
        self.base_ceviklik = self.attribute_component.hiz * 0.5
        self.base_tasima_limiti = self.attribute_component.guc * 2.5
