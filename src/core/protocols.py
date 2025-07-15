from typing import Protocol
from core.enums import OyuncuSlotu
from core.datatypes import ItemProto
from systems.components.equipment import EquipmentComponent
from systems.components.inventory import InventoryComponent
from systems.components.location import LocationComponent

class HasCombatStats(Protocol):
    can: int
    def saldiri_gucu(self, el: OyuncuSlotu | None = None) -> int: ...
    @property
    def zirh(self) -> int: ...

class HasEquipment(Protocol):
    kusanilan: dict[OyuncuSlotu, ItemProto | None]

    def kusan(self, item_id: str, slot: OyuncuSlotu | None = None) -> None: ...
    def kusanma_kontrolu(self, item_id: str, slot: OyuncuSlotu | None = None) -> tuple[ItemProto, tuple[OyuncuSlotu, ...]]: ...

class HasEquipmentComponent(Protocol):
    ekipman: EquipmentComponent

class HasInventoryComponent(Protocol):
    envanter: InventoryComponent

class HasLocationComponent(Protocol):
    konum: LocationComponent