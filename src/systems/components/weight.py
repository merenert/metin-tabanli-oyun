
from core.entity import Entity
from systems.components.attributes import AttributeComponent
from systems.components.stats import StatsComponent
from veriler.data_repo import ITEMS


class WeightComponent:
    def __init__(self, sahip: Entity):
        self.sahip = sahip

    def toplam_agirlik(self) -> float:
        from systems.components.inventory import InventoryComponent
        toplam = 0.0
        for item_id, miktar in self.sahip.al(InventoryComponent).inventory.items():
            item = ITEMS[item_id]
            if item:
                toplam += item.agirlik * miktar
        return toplam

    def yuzde_hesapla(self) -> float:
        tasimalimiti = self.sahip.al(StatsComponent).base_tasima_limiti
        if tasimalimiti <=  0 :
            return 0
        return (self.toplam_agirlik() / tasimalimiti) * 100

    def kapasite_doldu(self) -> bool:
        return self.toplam_agirlik() > self.sahip.stats.base_tasima_limiti

    def kalan_limit(self)  -> float:
        tasimalimiti = self.sahip.al(StatsComponent).base_tasima_limiti
        tasimalimiti -= self.toplam_agirlik()
        return tasimalimiti

    def apply_penalty_to_attributes(self):
        attr = self.sahip.al(AttributeComponent)
        yuzde = self.yuzde_hesapla()

        if yuzde <= 100:
            return  # Ceza yok

        oran = min((yuzde - 100) / 20, 1.0)  # 0.0 – 1.0 arası ceza oranı

        # Ağırlığa bağlı cezayı attribute değerlerine uygula
        attr.guc *= (1 - oran * 0.6) # Güç %60 oranında etkilenir
        if attr.guc < 1:
            attr.guc = 0.0
        attr.hiz *= (1 - oran * 0.8)  # Çeviklik daha fazla etkilenir
        if attr.hiz < 1:
            attr.hiz = 0.0
        attr.dayaniklilik *= (1 - oran * 0.5)
        if attr.dayaniklilik < 1:
            attr.dayaniklilik = 0.0

        # Attribute’lar düştüğü için Stats yeniden hesaplanmalı
        self.sahip.al(StatsComponent).update()

    def to_dict(self):
        return {
            "toplam_agirlik": self.toplam_agirlik(),
            "kalan_limit": self.kalan_limit(),
            "agirlik_yuzdesi": self.yuzde_hesapla()
        }






