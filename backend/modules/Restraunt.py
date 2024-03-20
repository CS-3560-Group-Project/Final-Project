# restraunt class
from backend.modules import Hours
from backend.modules import Location

class Restraunt:

    def __init__(self, name: str, location: Location, hours: 'list[Hours]') -> None:
        self.name = name
        self.location = location
        self.hours = hours

        self.rating = 0