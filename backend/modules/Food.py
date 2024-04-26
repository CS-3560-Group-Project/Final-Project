# food class
from modules.Restaurant import Restaurant

class Food:

    def __init__(self, restraunt: Restaurant, name: str, price: float, description: str, isBeverage: bool) -> None:
        self.restraunt = restraunt
        self.name = name
        self.price = price
        self.description = description
        self.isBeverage = isBeverage

    