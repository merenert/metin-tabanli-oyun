from typing import Dict, Optional , Self
class Envanter:
    def __init__(self):
        self.inventory: dict[str,int]= {}

    def ekle(self, item_id: str, adet: int = 1):
        if adet <= 0:
            raise ValueError("adet pozitif olmalı")
        self.inventory[item_id] = self.inventory.get(item_id, 0) + adet

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
    def miktar(self, item_id: str) -> int:
        return self.inventory.get(item_id, 0)

    def list_idleri(self) -> list[str]:
        return list(self.inventory.keys())