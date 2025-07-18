from systems.character import Karakter
from core.enums import OyuncuSlotu
from systems.eventbus import event_bus
from veriler.data_repo import RACES, CLASSES
from systems.components.equipment import EquipmentComponent
from systems.components.stats import StatsComponent
from systems.components.inventory import InventoryComponent
from systems.components.location import LocationComponent
from systems.components.attributes import AttributeComponent
from systems.components.weight import WeightComponent


class Karakterolusturucu:

    @staticmethod
    def karakterolustur(
        name: str,
        race_id: str,
        class_id: str,
        baslangic_bolge: str = "Sisli Koy",
        hand: OyuncuSlotu | None = None
    ) -> Karakter:

        # --- 1. Irk ve sınıf bonuslarını al
        try:
            race = RACES[race_id]
        except KeyError:
            raise ValueError(f"Geçersiz ırk: {race_id}")

        try:
            klass = CLASSES[class_id]
        except KeyError:
            raise ValueError(f"Geçersiz sınıf: {class_id}")

        # --- 2. Nitelikleri topla
        attributes = {}
        for attr in ["guc", "zeka", "hiz", "dayaniklilik"]:
            attributes[attr] = float(getattr(race, attr, 0) + getattr(klass, attr, 0))

        dom = hand or race.dominant_el

        # --- 3. Karakter nesnesi oluştur
        karakter = Karakter(
            isim=name,
            irk=race_id,
            sinif=class_id,
            dominant_el=dom
        )

        # --- 4. Component'leri karaktere ekle
        attribute_component = AttributeComponent(karakter, **attributes)
        karakter.ekle(attribute_component)
        karakter.ekle(StatsComponent(sahip=karakter, attribute_component=attribute_component))
        karakter.ekle(EquipmentComponent(karakter))
        karakter.ekle(InventoryComponent(karakter))
        karakter.ekle(LocationComponent(karakter, baslangic_bolge))
        karakter.ekle(WeightComponent(karakter))

        # --- 5. Olay yayını
        event_bus.publish("karakter_olustu", {
            "isim": name,
            "irk": race_id,
            "sinif": class_id
        })

        return karakter
