import json
import os
from systems.character import Karakter

KAYIT_DOSYASI = "save.json"

def save(karakter: Karakter, dosya_yolu: str = KAYIT_DOSYASI):
    data = karakter.to_dict()
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load(dosya_yolu: str = KAYIT_DOSYASI) -> Karakter:
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Karakter.from_dict(data)

def exists(dosya_yolu: str = KAYIT_DOSYASI) -> bool:
    return os.path.exists(dosya_yolu)