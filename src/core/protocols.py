from typing import Protocol
from core.enums import OyuncuSlotu
from core.inventory import Envanter
from core.datatypes import ItemProto

class HasCombatStats(Protocol):
    zirh: int
    can: int
    def saldiri_gucu(self, el: OyuncuSlotu | None = None) -> int: ...

class HasInventory(Protocol):
    envanter: Envanter

class HasEquipment(Protocol):
    kusanilan: dict[OyuncuSlotu, ItemProto | None]

    def kusan(self, item_id: str, slot: OyuncuSlotu | None = None) -> None: ...
    def kusanma_kontrolu(self, item_id: str, slot: OyuncuSlotu | None = None) -> tuple[ItemProto, tuple[OyuncuSlotu, ...]]: ...