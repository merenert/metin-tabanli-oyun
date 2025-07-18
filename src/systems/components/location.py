from core.datatypes import MapRegion
from systems.eventbus import event_bus
from systems.components.attributes import AttributeComponent
class LocationComponent:
    def __init__(self, sahip, baslangic_bolge: str):
        self.sahip = sahip
        self.bulundugu_bolge = baslangic_bolge

    def bolge_degistir(self, yeni_bolge: str, regions: dict[str, MapRegion]) -> bool:
        mevcut = regions[self.bulundugu_bolge]
        if yeni_bolge not in mevcut.komsular:
            return False
        if self.hareket_edebilir_mi():
            return False
        onceki = self.bulundugu_bolge
        self.bulundugu_bolge = yeni_bolge

        event_bus.publish("bolge_degisti", {
            "karakter": self.sahip,
            "onceki": onceki,
            "yeni": yeni_bolge
        })
        return True

    def hareket_edebilir_mi(self) -> bool:
        return self.sahip.al(AttributeComponent).hiz == 0 and self.sahip.al(AttributeComponent).dayaniklilik == 0

    def to_dict(self) -> dict:
        return {"bulundugu_bolge": self.bulundugu_bolge}

    @classmethod
    def from_dict(cls, sahip, data: dict):
        return cls(sahip, data["bulundugu_bolge"])