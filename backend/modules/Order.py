# order class
from backend.modules import Account
from backend.modules import BroncoBucks
from backend.modules import CreditCard
from backend.modules import Food

class Order:

    def __init__(self, account: Account, food: 'list[Food]', price: float, payment: BroncoBucks | CreditCard, isProcessing: bool) -> None:
        self.account = account
        self.food = food
        self.price = price
        self.payment = payment
        self.isProcessing = isProcessing

    #define change order status. changes the order status between pending, in process, and ready
    def changeOrderStatus(self, isProcessing: bool) -> None:
        pass

    # when order status is changed to being canceled, this method will cancel the order
    def cancelOrder(self) -> bool:
        pass