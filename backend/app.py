import os

# flask 
from flask import Flask, request, Response, render_template, redirect, url_for, jsonify
from database.queries import *

app = Flask(__name__)
HTML_PATH = os.path.dirname(__file__).replace("backend", "front") + "/pages"

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
        content = request.json

        # get form data
        email = content["email"]
        password = content["password"]

        # {"email": "jaron@gmail.con", "password": "12345"}
        
        data = getLoginQuery(email, password)[0]
        if len(data) > 0 and email in data and password in data:
            # redirect
            # return redirect(url_for("home"))
            return Response( "Logged in", status=200)
    
    # return get page
    # return render_template(f"{HTML_PATH}/login.html")
    return Response( "{Temporary response}", status=200)

@app.route("/create-account", methods = ["GET", "POST"])
def createAccount():
    # post data
    if request.method == "POST":
        content = request.json

        # post form data
        email = content["email"]
        password = content["password"]
        name = content["name"]

        nameOnCard = content["cardName"]
        cardNumber = content["cardNumber"]
        securityCode = content["cvv"]

        cardExpiration = content["cardExpiration"]
        cardExpirationMonth = cardExpiration[:2]
        cardExpirationYear = cardExpiration[2:]

        # post card id
        cardId = postCreditCardQuery(nameOnCard, cardNumber, securityCode, cardExpirationMonth, cardExpirationYear)
        if id != -1:
            # post account id
            accountId = postAccountQuery(cardId, email, password, name)
            if id == -1:
                return Response("Error creating account", status=404)

        # redirect to home
        # return redirect(url_for("home"))
        return Response( "Account created", status=201)
    
    # err
    return Response( "Invalid request type", status=404)

# MAIN PAGE TO SEE THE FOOD / RESTRAUNTS
@app.route("/home", methods = ["GET"])
def home():
    pass

@app.route("/food", methods = "POST")
def getRestaurants():
    # get request
    if request.method == "GET":
        content = request.json
        restaurantName = content["name"]

        restaurantFood = getFoodByRestaurantQueryName(restaurantName)
        foodData = {}

        for food in restaurantFood:
            # unpackage the food data
            foodID = food[0]
            restaurantID = food[1]
            foodName = food[2]
            description = food[3]
            price = food[4]
            foodImagePath = food[5]

            # append food data
            foodData[foodName] = {
                "foodID": foodID,
                "name": foodName,
                "description": description,
                "price": price,
                "foodImagePath": foodImagePath
            }

            return jsonify(foodData)

    # err
    return Response( "Invalid request type", status=404)

@app.route("/restaurant", methods = "POST")
def getRestaurants():
    # get request
    if request.method == "GET":
        allRestaurants = getAllRestaurantQuery()
        restaurantData = {}

        for restaurant in allRestaurants:
            # unpackage restaurant database
            restaurantID = restaurant[0]
            locationId = restaurant[1] # not used
            restaurantName = restaurant[2]
            hours = restaurant[3]
            restaurantImagePath = restaurant[4]
            numberReviews = restaurant[5]
            totalReviewScores = restaurant[6]

            # add all restaurant data to the json
            restaurantData[restaurantName] = {
                "restaurantId": restaurantID,
                "hours": hours,
                "reviews": {
                    "totalReviews": numberReviews,
                    "totalScore": totalReviewScores
                },
                "restaurantImagePath": restaurantImagePath
            }
        
        return jsonify(restaurantData)
    
    # err
    return Response( "Invalid request type", status=404)

@app.route("/restaurants-all", methods = ["GET"])
def getRestaurantsAll():
    # get request
    if request.method == "GET":
        allRestaurants = getAllRestaurantQuery()
        allRestaurantData = {}
        
        for restaurant in allRestaurants:
            # unpackage restaurant database
            restaurantID = restaurant[0]
            locationId = restaurant[1]
            restaurantName = restaurant[2]
            hours = restaurant[3]
            restaurantImagePath = restaurant[4]
            numberReviews = restaurant[5]
            totalReviewScores = restaurant[6]

            # get the location data
            allLocationData = getLocationQuery(locationId)
            locationId = allLocationData[0]
            buildingNumber = allLocationData[1]
            roomNumber = allLocationData[2]

            locationData = {
                "locationId": locationId,
                "buildingNumber": buildingNumber,
                "roomNumber": roomNumber
            }

            # get all the restaurant's food
            allFoodByRestaurant = getFoodByRestaurantQueryId(restaurantID)
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
            locationId = int(location[0])
            buildingNumber = location[1]
            roomNumber = location[2]

            locationData[locationId] = {
                "buildingNumber": buildingNumber,
                "roomNumber": roomNumber
            }

        return jsonify(locationData)
    # err
    return Response( "Invalid request type", status=404)

# RUN
if __name__ == "__main__":  
   app.run(debug=True, port=8080)