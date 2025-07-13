from dataclasses import dataclass, field
from typing import Dict, Optional , Self
from core.enums import OyuncuSlotu
from veriler import veriyukleyici
from systems.eventbus import EventBus, event_bus
from veriler.data_repo import RACES,CLASSES



class Karakterolusturucu:

    @staticmethod
    def karakterolustur(name: str, race_id: str, class_id: str,bulundugu_bolge:str,
                        hand: OyuncuSlotu | None = None) -> "Karakter":
        from systems.character import Karakter
        try:
            race = RACES[race_id]
        except KeyError:
            raise ValueError(f"Geçersiz ırk: {race_id}")

        try:
            klass = CLASSES[class_id]
        except KeyError:
            raise ValueError(f"Geçersiz sınıf: {class_id}")
        dom = hand or race.dominant_el

        event_bus.publish("karakter_olustu",{
            "isim": name,
            "irk": race_id,
            "sinif": class_id
        })

        return Karakter(
            isim=name,
            irk=race_id,
            sinif=class_id,
            can=race.can + klass.can,
            base_zirh=race.base_zirh,
            base_saldiri_gucu=race.base_saldiri_gucu + klass.base_saldiri_gucu,
            base_ceviklik=race.base_ceviklik + klass.base_ceviklik,
            bulundugu_bolge=bulundugu_bolge,
            dominant_el=dom

        )