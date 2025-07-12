from systems.character_factory import Karakterolusturucu
from systems import loglayici
from core import savegame

def main():
    loglayici.kaydol()  # olayları dinlemeye başla
    if savegame.exists():
        karakter = savegame.load()
        print(f"Kayıt yüklendi: {karakter.isim}")
    else:
        karakter = Karakterolusturucu.karakterolustur("Eldor", "elf", "okcu")
        savegame.save(karakter)
        print("Yeni karakter oluşturuldu ve kaydedildi.")

if __name__ == "__main__":
    main()



