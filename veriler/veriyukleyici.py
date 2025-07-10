import yaml
import os

from core.enums import OyuncuSlotu
from core.datatypes import RaceProto, ClassProto , ItemProto
from typing import cast

BASE_DIR = os.path.dirname(__file__)

def load_items():
    with open(os.path.join(BASE_DIR, "ITEMS.yaml"), encoding="utf-8") as f:
        rawitems = yaml.safe_load(f)

    return {
        key: ItemProto(
            id=key,
            name=veri["name"],
            slots=cast(tuple[OyuncuSlotu, ...], (OyuncuSlotu[s] for s in veri["slots"])),
            cift_el_kullan=veri.get("cift_el_kullan", False),
            zirh_bonusu=veri.get("zirh_bonusu", 0),
            hasar_bonusu=veri.get("hasar_bonusu", 0),
            engelleme=veri.get("engelleme", 0),
        )
        for key, veri in rawitems.items()
    }

def load_races():
    with open(os.path.join(BASE_DIR, "RACES.yaml"), encoding="utf-8") as f:
        rawraces = yaml.safe_load(f)


    return {
        key: RaceProto(
            id=key,
            can=veri["can"],
            base_zirh=veri["base_zirh"],
            base_saldiri_gucu=veri["base_saldiri_gucu"],
            ceviklik=veri["ceviklik"],
            dominant_el = cast(OyuncuSlotu, OyuncuSlotu[veri["dominant_el"]]),
        )
        for key, veri in rawraces.items()
    }

def load_classes():
    with open(os.path.join(BASE_DIR, "CLASSES.yaml"), encoding="utf-8") as f:
        rawclasses = yaml.safe_load(f)

    return {
        key: ClassProto(
            id=key,
            can=veri["can"],
            base_saldiri_gucu=veri["base_saldiri_gucu"],
            ceviklik=veri["ceviklik"],
            base_zirh=veri["base_zirh"],
        )
        for key, veri in rawclasses.items()
    }