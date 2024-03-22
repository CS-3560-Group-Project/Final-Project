# food class
from backend.modules import Restraunt

class Food:

    def __init__(self, restraunt: Restraunt, name: str, price: float, description: str, isBeverage: bool) -> None:
        self.restraunt = restraunt
        self.name = name
        self.price = price
        self.description = description
        self.isBeverage = isBeverage

    