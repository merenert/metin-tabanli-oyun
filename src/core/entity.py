class Entity:
    def __init__(self):
        self.components: dict[type, object] = {}

    def ekle(self, component: object):
        self.components[type(component)] = component
        if hasattr(component, "sahip"):
            component.sahip = self  # Geri bağlantı kurulabiliyorsa yap

    def al(self, component_tipi: type):
        return self.components.get(component_tipi, None)

    def has(self, component_tipi: type) -> bool:
        return component_tipi in self.components