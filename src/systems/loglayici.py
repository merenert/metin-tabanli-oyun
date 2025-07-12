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


def kaydol():
    event_bus.subscribe("karakter_olustu", karakter_olustu_log) #TODO: ŞU ANDA VAR OLAN BÜTÜN FONKSİYONLARA AYNISINI YAP #PYTEST KULLANMAYI ÖĞREN
    event_bus.subscribe("esya_ekledi", esya_ekledi_log)
    event_bus.subscribe("esya_kusandi", esya_kusandi_log)
    event_bus.subscribe("esya_cikardi", esya_cikardi_log)