from typing import Dict, Optional , Self
from systems.eventbus import event_bus

class InventoryComponent:
    def __init__(self, sahip = None):
        self.inventory: dict[str,int]= {}
        self.sahip = sahip

    def ekle(self, item_id: str, adet: int = 1):
        if adet <= 0:
            raise ValueError("adet pozitif olmalı")
        self.inventory[item_id] = self.inventory.get(item_id, 0) + adet

        event_bus.publish("esya_ekledi", {"karakter": self.sahip, "item_id": item_id})

    def cikart(self,item_id: str, adet: int = 1):
        if adet <= 0:
            raise ValueError("adet pozitif bir sayı olmalı")
        try:
            mevcut = self.inventory[item_id]
        except KeyError:
            raise ValueError("item envanterde yok")
        if adet > mevcut:
            raise ValueError(f"Envantede yalnızca {mevcut} adet var; {adet} çıkarılamaz")
        kalan = mevcut - adet
        if kalan:
            self.inventory[item_id] = kalan
        else:
            self.inventory.pop(item_id)

        event_bus.publish("esya_cikardi", {"karakter": self.sahip, "item_id": item_id})
    def miktar(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)

    def list_idleri(self) -> list[str]:
        return list(self.inventory.keys())


    def to_dict(self) -> dict:
        return self.inventory.copy()

    @classmethod
    def from_dict(cls, sahip, data: dict):
        inv = cls(sahip)
        inv.inventory = data.copy()
        return inv