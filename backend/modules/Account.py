# account class
from backend.modules import BroncoBucks
from backend.modules import CreditCard
class Account:

    def __init__(self, name: str, address: str, broncoPayment: BroncoBucks, cardPayment: 'list[CreditCard]') -> None:
        self.name = name
        self.address = address
        self.CreditCardPayment = cardPayment
        self.BroncoBucksPayment = broncoPayment
