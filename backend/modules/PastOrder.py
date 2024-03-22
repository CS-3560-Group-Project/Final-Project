# past order class
from backend.modules import Account
from backend.modules import BroncoBucks
from backend.modules import CreditCard
from backend.modules import Food
from backend.modules import Order

class PastOrder:

    def __init__(self, account: Account, food: 'list[Food]', price: float, payment: BroncoBucks | CreditCard) -> None:
        self.account = account
        self.food = food
        self.price = price
        self.payment = payment

    # creates a past order object
    def createPastOrder(self, pastOrder: Order) -> None:
        pass