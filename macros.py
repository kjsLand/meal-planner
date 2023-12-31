class ServingSize():
    __slots__ = ["__unit", "__value"]

    def __init__(self, unit:str, value:float):
        self.__unit = unit
        self.__value = value

    def __repr__(self) -> str:
        return str(self.__value)+self.__unit

class Products():
    __slots__ = [ "__name", "__serv_size", "__cals", "__fat", "__carbs", "__protein"]

    def __init__(self, name:str, cals:int, serv_size:ServingSize, fat:int, carbs:int, protein:int):
        self.__name = name
        self.__cals = cals
        self.__serv_size = serv_size
        self.__fat = fat
        self.__carbs = carbs
        self.__protein = protein

    def get_food(self, data=dict()):
        data[self.__name] = dict()
        data[self.__name]["cals"] = self.__cals
        data[self.__name]["serv_size"] = self.__serv_size
        data[self.__name]["fat"] = self.__fat
        data[self.__name]["carbs"] = self.__carbs
        data[self.__name]["protein"] = self.__protein
        return data
    
class Meal():
    __slots__ = ["__name", "__products"]

    def __init__(self, name:str, products:list):
        self.__name = name
        self.__products = products