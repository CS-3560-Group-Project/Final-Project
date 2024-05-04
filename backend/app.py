import os
from functools import wraps

# flask 
from flask import Flask, Response, session, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from database.queries import *

PORT = 5555
HTML_PATH = os.path.dirname(__file__).replace("backend", "front") + "/pages"

app = Flask(__name__, template_folder=HTML_PATH)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
app.secret_key = "a3898372693173f6f76191257ae22ba4416a3a067bb2ff9c4bbbd43bb4478057"

# Function to check if the user is logged in
# The only routes that require login are the cart functionalities and the checkout / account information
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedIn' not in session or not session['loggedIn']:
            return Response("Unauthorized", status=401)  # Return unauthorized status code
        return f(*args, **kwargs)
    return decorated_function

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

        # {"email": "jaron@gmail.con", "password": "12345"}
        
        data = getLoginQuery(email, password)[0]
        if len(data) > 0 and email in data and password in data:
            # add to session
            session["loggedIn"] = True
            session["userId"] = data[0] # index 0 is where the account id is stored

            # redirect
            # return redirect(url_for("home"))
            return Response( "Logged in", status=200)
    
    # return get page
    # return render_template(f"{HTML_PATH}/login.html")
    return Response( "{Temporary response}", status=200)

# This is the logout route where you are logged out and the session is cleared
@app.route('/logout', methods = ["GET"])
def logout():
    if request.method == "GET":
        # clear session data to log out
        session.clear()

        return Response("Logged out", status=200)
        # return redirect(url_for('index'))
    # err
    return Response( "Invalid request type", status=404)

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
@app.route("/accountPage", methods = ["GET"])
def getAccount():
    #get account data
    if request.method == "GET":
        acc = getAccountQuery(session["userId"])
        accData = {}

        for account in acc:
            #get account database info
            accountID = account[0]
            cardNum = account[1]
            email = account[2]
            password = account[3]
            name = account[4]

            #get card info query
            card = getCreditCardQuery(cardNum)
            cardData = {}
            for credit in card:
                #get credit card details
                cardID = credit[0]
                cardName = credit[1]
                cardNumber = credit[2]
                cardCode = credit[3]
                cardExpMon = credit[4]
                cardExpYr = credit[5]

            #add info to json
            accData[name] = {
                "name": name,
                "email": email,
                "password": password,
                "name": name,
                "card": cardNumber
            }

        return jsonify(accData)
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

            locationData[locationId] = {
                "buildingNumber": buildingNumber,
                "roomNumber": roomNumber
            }

        return jsonify(locationData)
    # err
    return Response("Invalid request type", status=404)

## CART AND ORDER API ##

# This is the add to cart route to add food given a foodId
@app.route("/addCart/<foodId>", methods=["POST"])
@login_required
def add_to_cart(foodId):
    if request.method == "POST":
        if "cart" not in session:
            session["cart"] = []

        session["cart"].append(foodId)
        session["cart"] = session["cart"]
        #print(f"Updated cart: {session["cart"]}")
        return Response("Item added to cart", status=200)
    else:
        return Response("Invalid request type", status=405)  # Method Not Allowed
    
# This route will help with seeing the food in the cart
@app.route("/cart", methods = ["GET"])
# @login_required
@cross_origin()
def cart():
    if request.method == "GET":
        cartItems = session.get("cart", [])
        cartData = {}
        
        # get card items
        for cartFoodId in cartItems:
            foodData = getFoodQuery(cartFoodId)[0]

            # unpackage the food data
            foodID = foodData[0]
            restaurantID = foodData[1]
            foodName = foodData[2]
            description = foodData[3]
            price = foodData[4]
            foodImagePath = foodData[5]

            # check if we need to update quantity
            if foodName in cartData:
                cartData[foodName]["quantity"] += 1
            else:
                # append food data
                cartData[foodName] = {
                    "id": foodID,
                    "name": foodName,
                    "description": description,
                    "price": float(price),
                    "quantity": 1,
                    "img": foodImagePath
                }

        return jsonify(cartData)
    # err
    return Response("Invalid request type", status=404)

# RUN
if __name__ == "__main__":  
   app.run(debug=True, port=PORT)