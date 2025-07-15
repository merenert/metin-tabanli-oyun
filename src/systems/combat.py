
from systems.eventbus import event_bus
from core.protocols import HasCombatStats


class CombatSystem:
    def __init__(self):
        pass

    @staticmethod
    def hasar_hesapla(hedef: HasCombatStats, gelen_hasar: int) -> int:
        net_hasar = max(0, gelen_hasar - hedef.zirh)
        return net_hasar

    def saldir(self, saldiran:HasCombatStats, hedef:HasCombatStats, el):
        saldiri_gucu = saldiran.saldiri_gucu(el)
        net_hasar = self.hasar_hesapla(hedef, saldiri_gucu)
        hedef.can -= net_hasar
        event_bus.publish("saldiri_yapildi", {
            "saldiran": saldiran,
            "hedef": hedef,
            "hasar": net_hasar,
            "el": el
        })
        return net_hasar


