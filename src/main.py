from systems.character_factory import Karakterolusturucu
from systems import loglayici

def main():
    loglayici.kaydol()  # olayları dinlemeye başla

    karakter = Karakterolusturucu.karakterolustur("Eldor", "elf", "okcu")
    print("Karakter başarıyla oluşturuldu:", karakter.isim)

if __name__ == "__main__":
    main()




