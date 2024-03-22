# shopping cart classs
from backend.modules import Account
from backend.modules import Food
from backend.modules import Order

class ShoppingCart:

    def __init__(self, account: Account, food: 'list[Food]', price: float) -> None:
        self.account = account
        self.food = food
        self.price = price

    # takes in a food object to add to the users cart
    def addToCart(self, foodItem: Food) -> bool:
        pass

    # this will process the payment between the account and cart total
    # it will create and return an order object
    def processPayment(self) -> Order:
        pass