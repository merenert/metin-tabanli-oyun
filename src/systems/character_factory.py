from dataclasses import dataclass, field
from typing import Dict, Optional , Self
from core.enums import OyuncuSlotu
from systems.character import Karakter

class Karakterolusturucu:
    @staticmethod
    def karakterolustur(name: str, race_id: str, class_id: str,
                        hand: OyuncuSlotu | None = None) -> Karakter:
        try:
            race = RACES[race_id]
        except KeyError:
            raise ValueError(f"Geçersiz ırk: {irk_id}")

        try:
            klass = CLASSES[class_id]
        except KeyError:
            raise ValueError(f"Geçersiz sınıf: {class_id}")
        dom = hand or race.dominant_el

        event_bus.publish("karakter_olustu", {
            "isim": isim,
            "irk": irk_id,
            "sinif": sinif_id
        })

        return Karakter(
            isim=name,
            irk=race_id,
            sinif=class_id,
            can=race.can + klass.can,
            base_zirh=race.base_zirh,
            base_saldiri_gucu=race.base_saldiri_gucu + klass.base_saldiri_gucu,
            ceviklik=race.ceviklik + klass.ceviklik,
            dominant_el=dom,
        )