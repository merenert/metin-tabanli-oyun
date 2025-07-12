from systems.eventbus import event_bus

def karakter_olustu_log(data):
    print(f" Karakter oluşturuldu: {data['isim']} (ırk: {data['irk']}, sınıf: {data['sinif']})")

def esya_ekledi_log(data):
    karakter = data["karakter"]
    item_id = data["item_id"]
    print(f"[Log] {karakter.isim} envanterine {item_id} eşyasını ekledi.")

def esya_cikardi_log(data):
    karakter = data["karakter"]
    item_id = data["item_id"]
    print(f"[Log] {karakter.isim} envanterinden {item_id} eşyasını çıkarttı.")

def esya_kusandi_log(data):
    karakter = data["karakter"]
    item_id = data["item_id"]
    el = data.get("el", "belirtilmemiş")
    print(f"[Log] {karakter.isim}, {el} eline {item_id} eşyasını kuşandı.")

def saldiri_yapildi_log(data):
    saldiran = data["saldiran"]
    hedef = data["hedef"]
    el = data["el"]
    print(f"[Log] {saldiran.isim}, {hedef.isim} kişisine {el} ile saldırdı")

def tur_basladi_log(data):
    tur = data["tur"]
    print(f"[Log] Tur başladı: {tur}")

def sira_degisti_log(data):
    onceki = data["onceki"]
    yeni = data["yeni"]
    tur = data["tur"]
    print(f"[Log] {onceki.isim} kişisinin sırası bitti, sıra {yeni.isim} kişisinde, tur: {tur} ")
def kaydol():
    event_bus.subscribe("karakter_olustu", karakter_olustu_log)
    event_bus.subscribe("esya_ekledi", esya_ekledi_log)
    event_bus.subscribe("esya_kusandi", esya_kusandi_log)
    event_bus.subscribe("esya_cikardi", esya_cikardi_log)
    event_bus.subscribe("saldiri_yapildi", saldiri_yapildi_log)
    event_bus.subscribe("tur_basladi", tur_basladi_log)
    event_bus.subscribe("sira_degisti", sira_degisti_log)