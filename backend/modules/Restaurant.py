# restaurant class
from backend.modules import Food
from backend.modules import Hours
from backend.modules import Location
from backend.modules import Order
from backend.modules import Review

class Restaurant:

    def __init__(self, name: str, location: Location, hours: 'list[Hours]',  food: 'list[Food]', ratings: 'list[Review]') -> None:
        self.name = name
        self.location = location
        self.hours = hours
        self.foodItems = food
        self.ratings = ratings

    # returns an array of Food objects that belong to the class
    def getFoodItems(self) -> 'list[Food]':
        pass

    # searches restaurant for a specific food item
    #   foodName = String
    #   foodType = Bool (true = food, false = drink)
    def searchFood(self, foodName=None, foodType=None):
        pass

    # creates a food object and adds it to self.food
    def addMenuItem(self, foodItems: Food) -> None:
        pass

    # searches through self.food for item to edit
    def editMenuItem(self, foodItem: Food) -> None:
        pass

    # searches through self.food and deletes object
    def deleteMenuItem(self, foodItem: Food) -> None:
        pass

    def recieveOrder(self, Order) -> None:
        pass

    # adds a review to the ratings
    def addReview() -> None:
        pass

    # goes through self.ratings and add the score
    def getRatingScore() -> int:
        pass