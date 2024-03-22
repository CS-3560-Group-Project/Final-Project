# bronco bucks class

class BroncoBucks:
 
    def __init__(self, name: str, idNumber: int, balance: float = 0.0) -> None:
        self.broncoAccountName = name
        self.broncoIdNumber = idNumber
       
    # this will charge the bronco account the order total
    def chargePayment(self) -> None:
        pass
    