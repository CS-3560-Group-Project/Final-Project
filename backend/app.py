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
                "foodID": foodID,
                "name": foodName,
                "description": description,
                "price": price,
                "foodImagePath": foodImagePath
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
        print(session["cart"])
        return Response("Item added to cart", status=200)
    else:
        return Response("Invalid request type", status=405)  # Method Not Allowed

# Remove from cart route
@app.route("/removeCart/<foodId>", methods=["POST"])
@login_required
def remove_from_cart(foodId):   
    if request.method == "POST":
        if "cart" in session and foodId in session["cart"]:
            new_cart = []
            for item in range(len(session["cart"])):
                if item != foodId: session["cart"].append(item)
            session["cart"] = new_cart
            print(session["cart"])
            return Response("Item removed from cart", status=200)
        elif "cart" not in session:
            return Response("Cart is empty", status=404)
        else:
            return Response("Item not in cart", status=404)
    else:
        return Response("Invalid request type", status=405)
    
# This route will help with seeing the food in the cart
@app.route("/cart", methods = ["GET"])
# @login_required
@cross_origin()
def cart():
    if request.method == "GET":
        cartItems = session.get("cart", [])
        cartItems = {
        "Qdoba": {
            "location": {
                "buildingNumber": "35",
                "roomNumber": "0"
            },
            "name": "Qdoba",
            "img": "https://content-service.sodexomyway.com/media/qdoba-logo_tcm146-6733_w1920_h976.jpg?url=https://www.ncatdining.com/",
            "food": [
                {
                    "name": "Mexican Street Corn Shrimp Bowl",
                    "description": "Citrus Lime Shrimp and new, warm Mexican Street Corn topped with chile crema, guacamole, pickled red onions, cotija cheese and chopped cilantro, served over cilantro lime rice and black beans.",
                    "price": 11.95,
                    "quantity": 5,
                    "img": "https://olo-images-live.imgix.net/73/73d4977998dd4883a08d0b20108c3fca.jpeg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1050&h=699&fit=fill&fm=png32&bg=transparent&s=11bb860c592f3487a7d883aad9becd96"
                },
                {
                    "name": "Cholula® Hot & Sweet Chicken Bowl",
                    "description": "Cholula® Hot & Sweet Chicken with pico de gallo, cilantro lime rice, black beans, sour cream, and cotija cheese.",
                    "price": 10.45,
                    "quantity": 1,
                    "img": "https://olo-images-live.imgix.net/89/89eea6e2b1684666afb93576c8a0f964.jpg?auto=format%2Ccompress&q=60&cs=tinysrgb&w=1050&h=699&fit=fill&fm=png32&bg=transparent&s=3da1160f0d26b5790b9c44aadf487392"
                }
            ]
        }
    }
        return jsonify(cartItems)
    # err
    return Response("Invalid request type", status=404)

# RUN
if __name__ == "__main__":  
   app.run(debug=True, port=PORT)