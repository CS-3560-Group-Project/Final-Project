# account class
from backend.modules import BroncoBucks
from backend.modules import CreditCard
from backend.modules import Location
class Account:

    def __init__(self, name: str, location: Location, broncoPayment: BroncoBucks, cardPayment: 'list[CreditCard]') -> None:
        self.name = name
        self.address = address
        self.CreditCardPayment = cardPayment
        self.BroncoBucksPayment = broncoPayment
