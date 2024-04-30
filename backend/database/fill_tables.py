import json, time
from queries import *

def fillAll():
    with open("backend/dummy/location.json") as FILE:
        data = json.load(FILE)["locations"]

        for location in data:
            postLocationQuery(location["buildingNumber"], location["roomNumber"])

    print("added locations...")
    time.sleep(2)

    with open("backend/dummy/restaurant.json") as FILE:
        data = json.load(FILE)

        for name, nameData in data.items():
            # get location
            locations = getAllLocationQuery()
            locationId = None

            for locationIds in locations:
                if nameData["location"]["buildingNumber"] == locationIds[1] and nameData["location"]["roomNumber"] == locationIds[2]:
                    locationId = locationIds[0]
                    break

            postRestaurantQuery(
                locationId,
                name,
                nameData["hours"],
                nameData["img"],
                nameData["numberReviews"],
                nameData["totalReviewScore"],
            )
    
    print("added restaurants...")
    time.sleep(2)

    with open("backend/dummy/food.json") as FILE:
        data = json.load(FILE)

        for name, nameData in data.items():
            restaurants = getAllRestaurantQuery()
            restaurantId = None

            for restaurantIds in restaurants:
                if name == restaurantIds[2]:
                    restaurantId = restaurantIds[0]
                    break

            for foodData in nameData:
                postFoodQuery(
                    restaurantId,
                    foodData["name"],
                    foodData["description"],
                    foodData["price"],
                    foodData["img"],
                )

    print("added foods...")

fillAll()