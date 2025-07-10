from systems.eventbus import event_bus

def karakter_olustu_log(data):
    print(f" Karakter oluşturuldu: {data['isim']} (ırk: {data['irk']}, sınıf: {data['sinif']})")

def kaydol():
    event_bus.subscribe("karakter_olustu", karakter_olustu_log) #TODO: ŞU ANDA VAR OLAN BÜTÜN FONKSİYONLARA AYNISINI YAP #PYTEST KULLANMAYI ÖĞREN