import mysql.connector

HOST = "localhost"
USER = "tannaz"
PASSWORD = "damavandi"
DATABASE_NAME = "FoodDelivery"

## SETUP ##
def connectDB():
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    return mydb

# Execute a query and fetch results
def queryTo(sql, params):
    mydb = connectDB()
    mycursor = mydb.cursor()
   
    try:
        mycursor.execute(sql, params)
        data = mycursor.fetchall()
   
        return data
   
    except mysql.connector.Error as err:
        print(f"Error: {err}")
   
        return None
   
    finally:
        mycursor.close()
        mydb.close()

# Execute an insert/update/delete query
def insertTo(sql, vals):
    mydb = connectDB()
    mycursor = mydb.cursor()
   
    try:
        mycursor.execute(sql, vals)
        id = mycursor.lastrowid
        mydb.commit()
   
    except mysql.connector.Error as err:
        id = -1
        print(f"Error: {err}")
   
    finally:
        mycursor.close()
        mydb.close()
    
    return id


## GET QUERIES ##
def getCreditCardQuery(cardID):
    sql = "SELECT * FROM CreditCard WHERE CardID = %s"
    data = queryTo(sql, (cardID))

    return data

def getLoginQuery(username, password):
    sql = "SELECT * FROM Account WHERE (Username = %s AND Password = %s)"
    data = queryTo(sql, (username, password))

    return data

def getAccountQuery(accountID):
    sql = "SELECT * FROM Account WHERE AccountID = %s"
    data = queryTo(sql, (accountID))

    return data

def getLocationQuery(locationID):
    sql = "SELECT * FROM Location WHERE LocationID = %s"
    data = queryTo(sql, (locationID))

    return data

def getRestaurantQuery(restaurantID):
    sql = "SELECT * FROM Restaurant WHERE RestaurantID = %s"
    data = queryTo(sql, (restaurantID))

    return data

def getFoodQuery(foodID):
    sql = "SELECT * FROM Food WHERE FoodID = %s"
    data = queryTo(sql, (foodID))

    return data

def getOrderQuery(orderID):
    sql = "SELECT * FROM `Order` WHERE OrderID = %s"
    data = queryTo(sql, (orderID))

    return data

def getReviewQuery(reviewID):
    sql = "SELECT * FROM Review WHERE ReviewID = %s"
    data = queryTo(sql, (reviewID))

    return data


## POST QUERIES ##
def postCreditCardQuery(name, number, code, month, year):
    sql = "INSERT INTO CreditCard (NameOnCard, CardNumber, CardSecurityCode, CardExpirationMonth, CardExpirationYear) VALUES (%s, %s, %s, %s, %s)"
    id = insertTo(sql, (name, number, code, month, year))

def postAccountQuery(locationId, cardId, username, password, name, phone):
    sql = "INSERT INTO Account (LocationID, CardID, Username, Password, Name, PhoneNumber) VALUES (%s, %s, %s, %s, %s, %s)"
    id = insertTo(sql, (locationId, cardId, username, password, name, phone))
    return id

def postLocationQuery(buildingNumber, roomNumber):
    sql = "INSERT INTO Location (BuildingNumber, RoomNumber) VALUES (%s, %s)"
    id = insertTo(sql, (buildingNumber, roomNumber))
    return id

def postRestaurantQuery(locationId, name, hours):
    sql = "INSERT INTO Restaurant (LocationID, Name, Hours) VALUES (%s, %s, %s)"
    id = insertTo(sql, (locationId, name, hours))
    return id

def postFoodQuery(restaurantId, name, description, price):
    sql = "INSERT INTO Food (RestaurantID, Name, Description, Price) VALUES (%s, %s, %s, %s)"
    id = insertTo(sql, (restaurantId, name, description, price))
    return id

def postOrderQuery(restaurantId, customerId, orderDate, totalAmount):
    sql = "INSERT INTO `Order` (RestaurantID, CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s, %s)"
    id = insertTo(sql, (restaurantId, customerId, orderDate, totalAmount))
    return id

def postReviewQuery(restaurantId, customerId, rating, comment):
    sql = "INSERT INTO Review (RestaurantID, CustomerID, Rating, Comment) VALUES (%s, %s, %s, %s)"
    id = insertTo(sql, (restaurantId, customerId, rating, comment))
    return id