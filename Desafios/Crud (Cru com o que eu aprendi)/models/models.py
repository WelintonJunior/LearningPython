def __init__():
    pass

class Product:
    def __init__(self, id, name, value):
        self.__id = id
        self.name = name
        self.value = value
    
    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.name,
            "value": self.value,
        }