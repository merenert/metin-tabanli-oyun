from core.enums import OyuncuSlotu
from systems.character_factory import Karakterolusturucu
from core import savegame
from systems.combat import CombatSystem
from veriler import veriyukleyici
from systems.turnmanager import TurnManager
def test_save_load():
    # 1. İki karakter oluştur
    karakter1 = Karakterolusturucu.karakterolustur("Eldor", "elf", "okcu")
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
    karakter1.envanter.ekle(esyalar["iron sword"].item_id)
    karakter2.envanter.ekle(esyalar["iron sword"].item_id)
    karakter2.envanter.ekle(esyalar["wood shield"].item_id)
    karakter1.kusan(esyalar["iron sword"].item_id, slot=OyuncuSlotu.SAG_KOL)
    karakter2.kusan(esyalar["iron sword"].item_id, slot=None)
    assert karakter1.kusanilan[OyuncuSlotu.SAG_KOL].item_id == esyalar["iron sword"].item_id
    assert karakter2.kusanilan[OyuncuSlotu.SAG_KOL].item_id == esyalar["iron sword"].item_id
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

        # Aktif karakter saldırıyor
        hasar = combat_system.saldir(aktif_karakter, hedef, OyuncuSlotu.SAG_KOL)
        print(f"{aktif_karakter.isim} saldırdı, verilen hasar: {hasar}, {hedef.isim} kalan can: {hedef.can}")

        # Tur ve sıra güncelle
        turn_manager.sonraki()


if __name__ == "__main__":
    test_combat()


