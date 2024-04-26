import os

# flask 
from flask import Flask, request, Response, render_template, redirect, url_for, jsonify
from database.queries import *

# modules
from modules.Account import Account

app = Flask(__name__)
HTML_PATH = os.path.dirname(__file__).replace("backend", "front") + "/pages"
ACCOUNT = Account()

## ROUTES FOR THE APP ##

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

# ACCOUNT CODE
# When the method is a get request, it is collecting the 
#   data from the user. When the method is a post request,
#   the function is required to store data in database.
@app.route("/login", methods = ["GET", "POST"])
def login():
    # post data
    if request.method == "POST":
        # get form data
        username = request.form.get("username")
        password = request.form.get("password")
        
        data = getLoginQuery(username, password)
        if len(data) > 0 and username in data and password in data:
            # create account details
            ACCOUNT.createAccount({
                "accountId": data[0],
                "locationId": data[1],
                "cardId": data[2],
                "username": data[3],
                "password": data[4],
                "name": data[5],
                "phoneNumber": data[6]
            })
            # redirect
            return redirect(url_for("home"))
    
    # return get page
    return render_template(f"{HTML_PATH}/login.html")

@app.route("/create-account", methods = ["GET", "POST"])
def createAccount():
    # post data
    if request.method == "POST":
        # post form data
        locationId = request.form.get("username")
        cardId = request.form.get("username")
        username = request.form.get("username")
        password = request.form.get("username")
        name = request.form.get("username")
        phone = request.form.get("username")

        id = postAccountQuery(locationId, cardId, username, password, name, phone)
        if id == -1:
            return Response("Error creating account", status=404)

        # create account details
        ACCOUNT.createAccount({
            "accountId": id,
            "locationId": locationId,
            "cardId": cardId,
            "username": username,
            "password": password,
            "name": name,
            "phoneNumber": phone
        })

        # redirect
        return redirect(url_for("home"))
    
    # err
    return Response( "Invalid request type", status=404)

# MAIN PAGE TO SEE THE FOOD / RESTRAUNTS
@app.route("/home", methods = ["GET"])
def home():
    pass

@app.route("/restaurants-all", methods = ["GET"])
def getRestaurants():
    # get request
    if request.method == "GET":
        allRestaurants = getAllRestaurantQuery()
        allRestaurantData = {}
        
        for restaurant in allRestaurants:
            # unpackage restaurant database
            restaurantID = restaurant[0]
            locationID = restaurant[1]
            restaurantName = restaurant[2]
            hours = restaurant[3]
            restaurantImagePath = restaurant[4]
            numberReviews = restaurant[5]
            totalReviewScores = restaurant[6]

            # get the location data
            allLocationData = getLocationQuery(locationID)
            locationID = allLocationData[0]
            buildingNumber = allLocationData[1]
            roomNumber = allLocationData[2]

            locationData = {
                "locationID": locationID,
                "buildingNumber": buildingNumber,
                "roomNumber": roomNumber
            }

            # get all the restaurant's food
            allFoodByRestaurant = getFoodByRestaurantQuery(restaurantID)
            foodData = []

            for food in allFoodByRestaurant:
                # unpackage the food data
                foodID = food[0]
                restaurantID = food[1]
                foodName = food[2]
                description = food[3]
                price = food[4]
                foodImagePath = food[5]

                # append food data
                foodData.append({
                    "foodID": foodID,
                    "name": foodName,
                    "description": description,
                    "price": price,
                    "foodImagePath": foodImagePath
                })

            # add all restaurant data to the json
            allRestaurantData[restaurantName] = {
                "restaurantId": restaurantID,
                "food": foodData,
                "hours": hours,
                "location": locationData,
                "reviews": {
                    "totalReviews": numberReviews,
                    "totalScore": totalReviewScores
                },
                "restaurantImagePath": restaurantImagePath
            }

        return jsonify(allRestaurantData)

    # err
    return Response( "Invalid request type", status=404)

# EXTRA ENDPOINTS
@app.route("/locations", methods = ["GET"])
def getLocations():
    if request.method == "GET":
        # get all the location data
        locations = getAllLocationQuery()
        locationData = {}

        for location in locations:
            # unpackage database
            locationID = int(location[0])
            buildingNumber = location[1]
            roomNumber = location[2]

            locationData[locationID] = {
                "buildingNumber": buildingNumber,
                "roomNumber": roomNumber
            }

        return jsonify(locationData)
    # err
    return Response( "Invalid request type", status=404)

# RUN
if __name__ == "__main__":  
   app.run()