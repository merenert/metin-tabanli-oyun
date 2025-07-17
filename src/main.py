from core.enums import OyuncuSlotu
from systems.character_factory import Karakterolusturucu
from core import savegame
from systems.combat import CombatSystem
from veriler import veriyukleyici
from systems.turnmanager import TurnManager
from systems.components.equipment import EquipmentComponent
from systems.components.stats import StatsComponent
from systems.components.inventory import InventoryComponent
from systems.components.location import LocationComponent
from systems.components.attributes import AttributeComponent
from core.entity import Entity
from veriler.data_repo import ITEMS,CLASSES,REGIONS,RACES
def test_save_load():
    # 1. İki karakter oluştur
    karakter1 = Karakterolusturucu.karakterolustur("Eldor", "elf", "okcu",hand=OyuncuSlotu.SAG_KOL)
    karakter2 = Karakterolusturucu.karakterolustur("Balin", "ork", "okcu")

    # 2. Karakterleri kaydet
    savegame.save(karakter1, "karakter1.json")
    savegame.save(karakter2, "karakter2.json")

    # 3. Karakterleri yükle
    yuklenen1 = savegame.load("karakter1.json")
    yuklenen2 = savegame.load("karakter2.json")

    # 4. Yüklenen karakterleri doğrula
    assert yuklenen1.isim == "Eldor"
    assert yuklenen2.isim == "Balin"

    print(f"Karakter 1: {yuklenen1.isim} başarıyla yüklendi.")
    print(f"Karakter 2: {yuklenen2.isim} başarıyla yüklendi.")
def test_equipment():
    esyalar = veriyukleyici.load_items()
    karakter1 = savegame.load("karakter1.json")
    karakter2 = savegame.load("karakter2.json")

    envanter1 = karakter1.al(InventoryComponent)
    envanter2 = karakter2.al(InventoryComponent)
    ekipman1 = karakter1.al(EquipmentComponent)
    ekipman2 = karakter2.al(EquipmentComponent)

    envanter1.ekle(esyalar["iron sword"].item_id)
    envanter2.ekle(esyalar["iron sword"].item_id)
    envanter2.ekle(esyalar["wood shield"].item_id)

    ekipman1.kusan(esyalar["iron sword"].item_id, slot=OyuncuSlotu.SAG_KOL)
    ekipman2.kusan(esyalar["iron sword"].item_id, slot=None)

    assert ekipman1.kusanilan[OyuncuSlotu.SAG_KOL].item_id == esyalar["iron sword"].item_id
    assert ekipman2.kusanilan[OyuncuSlotu.SAG_KOL].item_id == esyalar["iron sword"].item_id

    savegame.save(karakter1, "karakter1.json")
    savegame.save(karakter2, "karakter2.json")

def test_combat():
    karakter1 = savegame.load("karakter1.json")
    karakter2 = savegame.load("karakter2.json")
    turn_manager = TurnManager([karakter1, karakter2])
    combat_system = CombatSystem()
    for _ in range(4):
        aktif_karakter = turn_manager.siradaki()
        hedef = karakter2 if aktif_karakter == karakter1 else karakter1

        # Aktif karakterin stats bileşenini al
        aktif_stats = aktif_karakter.al(StatsComponent)
        hedef_stats = hedef.al(StatsComponent)

        # Aktif karakter saldırıyor
        hasar = combat_system.saldir(aktif_stats, hedef_stats, OyuncuSlotu.SAG_KOL)
        print(f"{aktif_karakter.isim} saldırdı, verilen hasar: {hasar}, {hedef.isim} kalan can: {hedef_stats.can}")

        # Tur ve sıra güncelle
        turn_manager.sonraki()

    savegame.save(karakter1, "karakter1.json")
    savegame.save(karakter2, "karakter2.json")


def test_map_system():
    regions = veriyukleyici.load_regions()
    karakter1 = savegame.load("karakter1.json")
    karakter2 = savegame.load("karakter2.json")  # örnek

    # Karakterin konum bileşenini al
    konum1 = karakter1.al(LocationComponent)

    konum1.bulundugu_bolge = "Sisli Koy"
    print(f"Başlangıç: {konum1.bulundugu_bolge}")

    konum1.bolge_degistir("Karanlık Orman", regions)
    print(f"Yeni konum: {konum1.bulundugu_bolge}")

    savegame.save(karakter1, "karakter1.json")
    savegame.save(karakter2, "karakter2.json")

def test_stats():
    karakter1 = savegame.load("karakter1.json")
    print(karakter1.al(StatsComponent))




if __name__ == "__main__":
      test_save_load()
    # test_equipment()
    #   test_combat()
    #   test_map_system()
    #  test_stats()