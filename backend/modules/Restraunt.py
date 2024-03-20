# restraunt class
from backend.modules import Hours

class Restraunt:

    def __init__(self, name: str, location: str, hours: 'list[Hours]') -> None:
        self.name = name
        self.location = location
        self.hours = hours

        self.rating = 0