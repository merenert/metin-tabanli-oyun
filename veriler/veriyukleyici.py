import yaml
import os
from core.enums import OyuncuSlotu,MapTuru
from core.datatypes import RaceProto, ClassProto , ItemProto
from typing import cast, Tuple
from core.datatypes import MapRegion

BASE_DIR = os.path.dirname(__file__)

def load_items():
    with open(os.path.join(BASE_DIR, "ITEMS.yaml"), encoding="utf-8") as f:
        rawitems = yaml.safe_load(f)

    return {
        key: ItemProto(
            item_id=key,
            name=veri["name"],
            slots=cast(tuple[OyuncuSlotu, ...], tuple(OyuncuSlotu[s] for s in veri["slots"])),
            cift_el_kullan=veri.get("cift_el_kullan", False),
            zirh_bonusu=veri.get("zirh_bonusu", 0),
            hasar_bonusu=veri.get("hasar_bonusu", 0),
            ceviklik_bonusu=veri.get("ceviklik_bonusu", 0),
            engelleme=veri.get("engelleme", 0),
            agirlik=veri.get("agirlik", 0)
        )
        for key, veri in rawitems.items()
    }

def load_races():
    with open(os.path.join(BASE_DIR, "RACES.yaml"), encoding="utf-8") as f:
        rawraces = yaml.safe_load(f)


    return {
        key: RaceProto(
            race_id=key,
            guc=veri["guc"],
            dayaniklilik=veri["dayaniklilik"],
            hiz=veri["hiz"],
            zeka=veri["zeka"],
            dominant_el = cast(OyuncuSlotu, OyuncuSlotu[veri["dominant_el"]]),
        )
        for key, veri in rawraces.items()
    }

def load_classes():
    with open(os.path.join(BASE_DIR, "CLASSES.yaml"), encoding="utf-8") as f:
        rawclasses = yaml.safe_load(f)

    return {
        key: ClassProto(
            class_id=key,
            guc=veri["guc"],
            dayaniklilik=veri["dayaniklilik"],
            hiz=veri["hiz"],
            zeka=veri["zeka"],
        )
        for key, veri in rawclasses.items()
    }
def load_regions(yaml_dosyasi_yolu: str = "REGIONS.yaml") -> dict[str, MapRegion]:
    with open(os.path.join(BASE_DIR, yaml_dosyasi_yolu), encoding="utf-8") as f:
        rawregions = yaml.safe_load(f)

    return {
        key: MapRegion(
            region_id=key,
            name=veri["isim"],
            komsular=veri.get("komsular", []),
            npc_idleri=veri.get("npc_idleri", []),
            map_turu=MapTuru(0) | sum((MapTuru[t] for t in veri.get("tur", [])), MapTuru(0)) ###
        )
        for key, veri in rawregions.items()
    }