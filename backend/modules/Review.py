# review class
from backend.modules import Account
from backend.modules import Restraunt

class Review:

    def __init__(self, restraunt: Restraunt, account: Account, score: int, description: str) -> None:
        self.restraunt = restraunt
        self.account = account
        self.score = score
        self.description = description

    # creates a review
    def createReview(self, restraunt: Restraunt, account: Account, score: int, description: str) -> None:
        pass