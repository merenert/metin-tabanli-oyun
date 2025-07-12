from systems.eventbus import event_bus

class TurnManager:
    def __init__(self, katilimcilar: list):
        self.katilimcilar = katilimcilar
        self.sira_indeksi = 0
        self.tur = 1
        event_bus.publish("tur_basladi", {"tur": self.tur})

    def siradaki(self):
        return self.katilimcilar[self.sira_indeksi]

    def sonraki(self):
        eski_karakter = self.siradaki()  # Mevcut sıradaki karakteri önce alıyoruz

        self.sira_indeksi += 1
        if self.sira_indeksi >= len(self.katilimcilar):
            self.sira_indeksi = 0
            self.tur += 1
            event_bus.publish("tur_basladi", {"tur": self.tur})

        yeni_karakter = self.siradaki()  # Yeni sıradaki karakteri alıyoruz

        event_bus.publish("sira_degisti", {
            "onceki": eski_karakter,
            "yeni": yeni_karakter,
            "tur": self.tur
        })

        return yeni_karakter

