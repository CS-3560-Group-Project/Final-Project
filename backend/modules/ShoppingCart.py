# shopping cart classs
from backend.modules import Account
from backend.modules import Food

class ShoppingCart:

    def __init__(self, account: Account, food: 'list[Food]', price: float) -> None:
        self.account = account
        self.food = food
        self.price = price