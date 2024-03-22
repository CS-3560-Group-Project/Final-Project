# account class
from backend.modules import BroncoBucks
from backend.modules import CreditCard
from backend.modules import Location

class Account:

    def __init__(self, name: str, location: Location, broncoPayment: BroncoBucks, cardPayment: 'list[CreditCard]') -> None:
        self.name = name
        self.location = location
        self.creditCardPayment = cardPayment
        self.broncoBucksPayment = broncoPayment

    # this will take in account details to create the account
    def createAccount(self, accountDetails: dict) -> None:
        pass

    # this will take in account details and create either a credit card payment or
    #   bronco bucks payment
    # it will be added to the class attributes
    def createPayment(self, accountDetails: dict) -> None:
        pass

    # adds credit card to payment
    def addCreditCard(self, creditCard: CreditCard) -> None:
        pass

    # adds bronco bucks to payment
    def addBroncoBucks(self, broncoBucks: BroncoBucks) -> None:
        pass

    # returns a list of all payment methods
    def viewPaymentMethods(self) -> 'list[BroncoBucks | CreditCard]':
        pass

    # when a order is being processed, the account will be charged
    # returns true when valid payment and false if the payment
    #   does not exist or is broke
    def processingPayment(self, paymentMethod: BroncoBucks | CreditCard) -> bool:
        pass

    