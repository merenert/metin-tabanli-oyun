from core.enums import OyuncuSlotu
from core.datatypes import ItemProto
from veriler.data_repo import ITEMS
from systems.eventbus import event_bus
from typing import cast



class EquipmentComponent:
    def __init__(self, sahip):
        self.sahip = sahip
        self.kusanilan: dict[OyuncuSlotu, ItemProto | None] = {
            slot: None for slot in OyuncuSlotu
        }
    # ====envanterden eşya kuşanma====
    def kusanma_kontrolu(self, item_id: str, slot: OyuncuSlotu | None = None) -> tuple[
        ItemProto, tuple[OyuncuSlotu, ...]]:
        from systems.components.inventory import InventoryComponent
        envanter = self.sahip.al(InventoryComponent)
        try:
            proto = ITEMS[item_id]
        except KeyError:
            raise ValueError(f"Geçersiz item id: {item_id}") from None

        if envanter.miktar(item_id) < 1:
            raise ValueError("Envanterde bu eşyadan yok")

        if len(proto.slots) > 1 and proto.cift_el_kullan and slot is not None:
            raise ValueError("Eşya çift el kullanıyor; slot seçilemez")

        if slot is not None and slot not in proto.slots:
            raise ValueError("Bu item belirtilen slota takılamaz")

        # Slot belirleme
        if len(proto.slots) > 1 and proto.cift_el_kullan:
            actual_slots = proto.slots
        else:
            if slot is None:
                if len(proto.slots) == 1:
                    actual_slots = proto.slots  # Tek slotlu eşya, kendi slotunu alır
                else:
                    chosen = self.sahip.dominant_el
                    if chosen not in proto.slots:
                        raise ValueError("Dominant el bu eşyayla uyuşmuyor")
                    actual_slots = (chosen,)
            else:
                # slot parametresi verilmiş, doğrula
                if slot not in proto.slots:
                    raise ValueError("Belirtilen slot bu eşya ile uyumlu değil")
                actual_slots = (slot,)

        # Doluluk kontrolü
        for s in actual_slots:
            if self.kusanilan.get(s) is not None:
                raise ValueError(f"{s.name} slotu dolu")

        return proto, actual_slots

    def kusan(self, item_id: str, slot: OyuncuSlotu | None = None):
        from systems.components.inventory import InventoryComponent
        proto, actual_slots = self.kusanma_kontrolu(item_id, slot)
        envanter = self.sahip.al(InventoryComponent)

        for s in actual_slots:
            self.kusanilan[s] = proto
            
            event_bus.publish("esya_kusandi", {
                "karakter": self,
                "item_id": proto,
                "el": s
            })
        envanter.cikart(item_id, 1)

    def to_dict(self) -> dict:
        # Slotlar enum olduğu için isimleri ile kaydediyoruz
        return {
            "kusanilan": {
                slot.name: item.item_id if item else None
                for slot, item in self.kusanilan.items()
            }
        }

    @classmethod
    def from_dict(cls, sahip, data: dict):
        ekipman = cls(sahip)
        kusanilan_data = data.get("kusanilan", {})
        for slot_name, item_id in kusanilan_data.items():
            slot = OyuncuSlotu[slot_name]
            if item_id is not None:
                # ITEMS sözlüğünden item protosunu çek
                item_proto = ITEMS.get(item_id)
                if item_proto:
                    ekipman.kusanilan[cast(OyuncuSlotu,slot)] = item_proto
        return ekipman