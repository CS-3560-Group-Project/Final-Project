# credit card class

class CreditCard:
    
    def __init__(self, name: str, number: int, securityCode: int, expirationMonth: int, expirationYear: int) -> None:
        self.name = name
        self.cardNumber = number
        self.cardSecurityCode = securityCode
        self.cardExpirationMonth = expirationMonth
        self.cardExpirationYear = expirationYear