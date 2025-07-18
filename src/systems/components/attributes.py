
class AttributeComponent:
    def __init__(
        self,
        sahip,
        guc: float ,
        zeka: float ,
        hiz: float ,
        dayaniklilik: float  ,
    ):
        self.sahip = sahip
        self.guc = guc
        self.zeka = zeka
        self.hiz = hiz
        self.dayaniklilik = dayaniklilik

    def to_dict(self) -> dict:
        return {
            "guc": self.guc,
            "zeka": self.zeka,
            "hiz": self.hiz,
            "dayaniklilik": self.dayaniklilik,
        }

    @classmethod
    def from_dict(cls, sahip, data: dict):
        return cls(
            sahip=sahip,
            guc=data.get("guc", 0),
            zeka=data.get("zeka", 0),
            hiz=data.get("hiz", 0),
            dayaniklilik=data.get("dayaniklilik", 0),
        )

