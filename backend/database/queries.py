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
        if params is not None: mycursor.execute(sql, params)
        else: mycursor.execute(sql)
        return mycursor.fetchall()
   
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

# Helper function to execute delete queries
def deleteRecord(sql, recordID):
    mydb = connectDB()
    mycursor = mydb.cursor()
    
    try:
        mycursor.execute(sql, (recordID,))
        mydb.commit()
        return True
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
    finally:
        mycursor.close()
        mydb.close()

# Helper function to execute update queries
def updateRecord(sql, params):
    mydb = connectDB()
    mycursor = mydb.cursor()
    
    try:
        mycursor.execute(sql, params)
        mydb.commit()
        return True
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
    finally:
        mycursor.close()
        mydb.close()


## GET QUERIES ##
def getCreditCardQuery(cardID):
    """Gets the data from the CreditCard table given a cardID."""
    sql = "SELECT * FROM CreditCard WHERE CardID = %s"
    return queryTo(sql, [cardID])

def getLoginQuery(email, password):
    """Gets the data from the Account table given a username and password."""
    sql = "SELECT * FROM Account WHERE (Email = %s AND Password = %s)"
    return queryTo(sql, [email, password])

def getAccountQuery(accountID):
    """Gets the data from the Account table given an accountID."""
    sql = "SELECT * FROM Account WHERE AccountID = %s"
    return queryTo(sql, [accountID])

def getAccountQueryEmail(email):
    """Gets the data from the Account table given an email."""
    sql = "SELECT * FROM Account WHERE Email = %s"
    return queryTo(sql, [email])

def getLocationQuery(locationID):
    """Gets the data from the Location table given a locationID."""
    sql = "SELECT * FROM Location WHERE LocationID = %s"
    return queryTo(sql, [locationID])

def getAllLocationQuery():
    """Gets all the data from the Location table."""
    sql = "SELECT * FROM Location"
    return queryTo(sql, None)

def getRestaurantQuery(restaurantID):
    """Gets the data from the Restaurant table given a restaurantID."""
    sql = "SELECT * FROM Restaurant WHERE RestaurantID = %s"
    return queryTo(sql, [restaurantID])

def getAllRestaurantQuery():
    """Gets all the data from the Restaurant table."""
    sql = "SELECT * FROM Restaurant"
    return queryTo(sql, None)

def getFoodQuery(foodID):
    """Gets the data from the Food table given a foodID."""
    sql = "SELECT * FROM Food WHERE FoodID = %s"
    return queryTo(sql, [foodID])

def getFoodByRestaurantQueryId(restaurantID):
    """Gets the data from the Food table given a restaurantID."""
    sql = "SELECT * FROM Food WHERE RestaurantID = %s"
    return queryTo(sql, [restaurantID])

def getFoodByRestaurantQueryName(restaurantName):
    """Gets the data from the Restaurant table given a restaurantID."""
    sql = "SELECT * FROM Restaurant WHERE Name = %s"
    return queryTo(sql, [restaurantName])

def getOrderQuery(orderID):
    sql = "SELECT * FROM Orders WHERE OrderID = %s"
    return queryTo(sql, [orderID])

def getOrderQueryByCustomer(CustomerID):
    sql = "SELECT * FROM Orders WHERE CustomerID = %s"
    return queryTo(sql, [CustomerID])

## POST QUERIES ##
def postCreditCardQuery(name, number, code, month, year):
    sql = "INSERT INTO CreditCard (NameOnCard, CardNumber, CardSecurityCode, CardExpirationMonth, CardExpirationYear) VALUES (%s, %s, %s, %s, %s)"
    return insertTo(sql, (name, number, code, month, year))

def postAccountQuery(cardId, email, password, name):
    sql = "INSERT INTO Account (CardID, Email, Password, Name) VALUES (%s, %s, %s, %s)"
    return insertTo(sql, (cardId, email, password, name))

def postLocationQuery(buildingNumber, roomNumber):
    sql = "INSERT INTO Location (BuildingNumber, RoomNumber) VALUES (%s, %s)"
    return insertTo(sql, (buildingNumber, roomNumber))

def postRestaurantQuery(locationId, name, hours, imagePath, numberReviews, totalReviews):
    sql = "INSERT INTO Restaurant (LocationID, Name, Hours, ImagePath, NumberReviews, TotalReviewScores) VALUES (%s, %s, %s, %s, %s, %s)"
    return insertTo(sql, (locationId, name, hours, imagePath, numberReviews, totalReviews))

def postFoodQuery(restaurantId, name, description, price, imagePath):
    sql = "INSERT INTO Food (RestaurantID, Name, Description, Price, ImagePath) VALUES (%s, %s, %s, %s, %s)"
    return insertTo(sql, (restaurantId, name, description, price, imagePath))

def postOrderQuery(restaurantId, locationId, customerId, orderDate, totalAmount):
    sql = "INSERT INTO Orders (RestaurantID, LocationID, CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s, %s, %s)"
    return insertTo(sql, (restaurantId, locationId, customerId, orderDate, totalAmount))


## DELETE QUERIES ##
def deleteCreditCardQuery(cardID):
    sql = "DELETE FROM CreditCard WHERE CardID = %s"
    return deleteRecord(sql, cardID)

def deleteAccountQuery(accountID):
    sql = "DELETE FROM Account WHERE AccountID = %s"
    return deleteRecord(sql, accountID)

def deleteLocationQuery(locationID):
    sql = "DELETE FROM Location WHERE LocationID = %s"
    return deleteRecord(sql, locationID)

def deleteRestaurantQuery(restaurantID):
    sql = "DELETE FROM Restaurant WHERE RestaurantID = %s"
    return deleteRecord(sql, restaurantID)

def deleteFoodQuery(foodID):
    sql = "DELETE FROM Food WHERE FoodID = %s"
    return deleteRecord(sql, foodID)

def deleteOrderQuery(customerID):
    sql = "DELETE FROM Orders WHERE CustomerID = %s"
    return deleteRecord(sql, customerID)

## UPDATE QUERIES ##
def updateAccountInformation(accountID, cardId, email, password, name):
    """This will update account information given an account ID."""
    sql = "UPDATE Account SET CardID = %s, Email = %s, Password = %s, Name = %s WHERE AccountID = %s"
    return updateRecord(sql, (cardId, email, password, name, accountID))

def updateCreditCardInformation(cardID, name, number, code, month, year):
    """This will update credit card information given an credit card ID."""
    sql = "UPDATE CreditCard SET NameOnCard = %s, CardNumber = %s, CardSecurityCode = %s, CardExpirationMonth = %s, CardExpirationYear = %s WHERE CardID = %s"
    return updateRecord(sql, (name, number, code, month, year, cardID))