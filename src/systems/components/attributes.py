
class AttributeComponent:
    def __init__(
        self,
        sahip,
        guc: float ,
        zeka: float ,
        ceviklik: float ,
        dayaniklilik: float  ,
    ):
        self.sahip = sahip
        self.guc = guc
        self.zeka = zeka
        self.ceviklik = ceviklik
        self.dayaniklilik = dayaniklilik

    def agirlik_limiti(self) -> float:
        return self.guc * 5  # Örnek: Her 1 güce karşılık 5 kg taşıma

    def base_can(self) -> float:
        return self.dayaniklilik * 10

    def base_zirh(self) -> float:
        return self.guc * 1.5  # Kas gücüyle gelen direnç

    def base_ceviklik(self) -> float:
        return self.ceviklik  # İsteğe göre formül eklenebilir

    def to_dict(self) -> dict:
        return {
            "guc": self.guc,
            "zeka": self.zeka,
            "ceviklik": self.ceviklik,
            "dayaniklilik": self.dayaniklilik,
        }

    @classmethod
    def from_dict(cls, sahip, data: dict):
        return cls(
            sahip=sahip,
            guc=data.get("guc", 0),
            zeka=data.get("zeka", 0),
            ceviklik=data.get("ceviklik", 0),
            dayaniklilik=data.get("dayaniklilik", 0),
        )

