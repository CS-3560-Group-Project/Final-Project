import os
from functools import wraps
from datetime import datetime

# flask 
from flask import Flask, Response, session, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from database.queries import *

PORT = 5555
HTML_PATH = os.path.dirname(__file__).replace("backend", "frontend") + "/pages"

app = Flask(__name__, template_folder=HTML_PATH)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

## ROUTES FOR THE APP ##

# This is the landing route which reroutes depending on if you are logged in
@app.route("/")
def index():
    # redirect to the home page if already logged in
    if "loggedIn" in session and session["loggedIn"] == True:
        return redirect(url_for('restaurants'))
    # redirect to login page if not logged in
    return redirect(url_for('login'))

# This is the login route for which you login with a email and a password
# The data comes from the frontend in teh form of json
@app.route("/login", methods = ["GET", "POST"])
def login():
    # post data
    if request.method == "POST":
        content = request.json

        # get form data
        email = content["email"]
        password = content["password"]

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400
        
        data = getLoginQuery(email, password)
        if len(data) > 0:
            data = data[0]
            if email in data and password in data:
                return jsonify({"id": data[0]}), 200
        else:
            return jsonify({"error": "Invalid email or password."}), 401
    
    return jsonify({"error": "Method not allowed."}), 405

# This is where we create an account bassed on the frontend
# The data comes in the from of json
@app.route("/create-account", methods = ["GET", "POST"])
def createAccount():
    # post data
    if request.method == "POST":
        content = request.json

        # post form data
        email = content["email"]
        password = content["password"]
        name = content["name"]

        locationId = content["location"] # this is not stored in the db
        print(locationId)

        nameOnCard = content["cardName"]
        cardNumber = content["cardNumber"]
        securityCode = content["cvv"]

        cardExpiration = content["cardExpiration"]
        cardExpirationMonth = cardExpiration[:2]
        cardExpirationYear = cardExpiration[2:]

        # check if the data is already existing
        accountExist = len(getAccountQueryEmail(email)) != 0
        if accountExist:
            return jsonify({"error": "Email already in use."}), 409

        # post card id
        cardId = postCreditCardQuery(nameOnCard, cardNumber, securityCode, cardExpirationMonth, cardExpirationYear)
        if id != -1:
            # post account id
            accountId = postAccountQuery(cardId, email, password, name)
            if id == -1:
                return jsonify({"error": "Error creating account."}), 404

        return jsonify({"id": accountId, "locationId": locationId}), 201
    # err
    return Response( "Invalid request type", status=404)

@app.route("/update-account", methods=["POST"])
def updateAccount():
    # Check if it's a POST request
    if request.method == "POST":
        content = request.json

        # Extract data from the request
        email = content.get("email")
        password = content.get("password")
        name = content.get("name")
        locationId = content.get("location") # this is not stored in the d
        cardName = content.get("cardName")
        cardNumber = content.get("cardNumber")
        cvv = content.get("cvv")
        cardExpiration = content.get("cardExpiration")
        cardExpirationMonth = cardExpiration[:2]
        cardExpirationYear = cardExpiration[2:]

        # Check if the account exists
        existing_account = getAccountQueryEmail(email)
        if not existing_account:
            return jsonify({"error": "Account does not exist."}), 404
        existing_account = existing_account[0]

        # card id
        cardId = int(existing_account[1])

        # Update the account information
        updated_card_id = updateCreditCardInformation(cardId, cardName, cardNumber, cvv, cardExpirationMonth, cardExpirationYear)
        if updated_card_id == -1:
            return jsonify({"error": "Error updating credit card information."}), 500

        # account id
        accountId = int(existing_account[0])

        updated_account_id = updateAccountInformation(accountId, cardId, email, password, name)
        if updated_account_id == -1:
            return jsonify({"error": "Error updating account information."}), 500
        
        return jsonify({"locationId": int(locationId)}), 200

    # Return error for invalid request type
    return jsonify({"error": "Invalid request type."}), 405

@app.route('/delete-account', methods=['POST'])
def deleteAccount():
    data = request.json
    accountId = data.get('id')

    accountData = getAccountQuery(accountId)
    if accountData:
        accountData = accountData[0]
        cardId = accountData[1]
        orders = getOrderQueryByCustomer(accountId)
        if deleteAccountQuery(accountId) and deleteCreditCardQuery(cardId) and (deleteOrderQuery(accountId) if orders else True):
            return '', 204  
    else:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({"error": "Error."}), 400

## MAIN PAGE TO SEE THE FOOD / RESTRAUNTS

# This is the page where given a restaurant you can view its food
@app.route("/<restaurantId>/food/", methods = ["GET"])
def getFood(restaurantId):
    # get request
    if request.method == "GET":
        restaurantFood = getFoodByRestaurantQueryId(restaurantId)
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
                "id": foodID,
                "name": foodName,
                "description": description,
                "price": float(price),
                "img": foodImagePath
            }

        return jsonify(foodData)
    # err
    return Response("Invalid request type", status=404)

# This is the page where you can see all the restaurants laid out
@app.route("/restaurants", methods = ["GET"])
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
                "name": restaurantName,
                "id": restaurantID,
                "hours": hours,
                "reviews": {
                    "totalReviews": numberReviews,
                    "totalScore": totalReviewScores
                },
                "img": restaurantImagePath
            }
        
        return jsonify(restaurantData)
    # err
    return Response("Invalid request type", status=404)

#Page for account details
@app.route("/account-page", methods = ["POSt"])
def getAccount():
    #get account data
    if request.method == "POST":
        try:
            content = request.json
            id = content["id"]
            acc = getAccountQuery(id)
            accData = {}
        except:
            return Response("Invalid request type", status=404)     

        for account in acc:
            #get account database info
            accountID = account[0]
            cardId = account[1]
            email = account[2]
            password = account[3]
            name = account[4]

            #get card info query
            card = getCreditCardQuery(cardId)
            cardData = {}
            for credit in card:
                #get credit card details
                cardId = credit[0]
                cardName = credit[1]
                cardNumber = credit[2]
                cvv = credit[3]
                cardExpMon = credit[4]
                cardExpYr = credit[5]

            #add info to json
            accData[name] = {
                "name": name,
                "email": email,
                "password": password,
                "cardholderName": cardName,
                "cardNumber": cardNumber,
                "expirationDate": f"{cardExpMon}{cardExpYr}",
                "CVV": cvv
            }
        return jsonify(accData), 200
    #error handling
    return Response("Invalid request type", status=404)     


# This is a route where you can get a list of all the location data 
# This is helpful for the drop down to select where the food will go
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

            if buildingNumber in locationData:
                locationData[buildingNumber].append({
                    "id": locationId,
                    "roomNumber": roomNumber
                })
            else:
                locationData[buildingNumber] = [{
                    "id": locationId,
                    "roomNumber": roomNumber
                }]

        return jsonify(locationData)
    # err
    return Response("Invalid request type", status=404)

## CART AND ORDER API ##
    
# This route will help with seeing the food in the cart
@app.route("/cart", methods = ["POST"])
@cross_origin()
def cart():
    if request.method == "POST":
        content = request.json # {foodId: quantity}
        cartData = {}
        
        # get card items
        for cartFoodId, quantity in content.items():
            foodData = getFoodQuery(cartFoodId)[0]

            # unpackage the food data
            foodID = foodData[0]
            restaurantID = foodData[1]
            foodName = foodData[2]
            description = foodData[3]
            price = foodData[4]
            foodImagePath = foodData[5]

            restaurantData = getRestaurantQuery(restaurantID)[0]
            restaurantName = restaurantData[2]

            # append food data
            cartData[foodName] = {
                "id": foodID,
                "name": foodName,
                "restaurant": {
                    "id": restaurantID,
                    "name": restaurantName
                },
                "description": description,
                "price": float(price),
                "quantity": int(quantity),
                "img": foodImagePath
            }

        return jsonify(cartData)
    # err
    return Response("Invalid request type", status=404)



# RUN
if __name__ == "__main__":  
   app.run(debug=True, port=PORT)