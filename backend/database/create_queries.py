
# MySQL
# https://www.mysql.com/downloads/]
# https://www.youtube.com/watch?v=ODA3rWfmzg8&ab_channel=ProgrammingKnowledge
# https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql

# Pip
# python -m pip install mysql-connector-python

# Imports
import mysql.connector

HOST = "localhost"
USER = "tannaz"
PASSWORD = "damavandi"
DATABASE_NAME = "FoodDelivery"

##### CREATE DATABASE #####

def createDatabase():
    # Connect to the databse
    mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    mycursor = mydb.cursor()

    # Create a database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS FoodDelivery")
    mycursor.close() # close cursor
    mydb.close() # close database

#createDatabase()

##### CREATE TABLES #####

def createTables():
    # Connect to the database
    mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME)
    mycursor = mydb.cursor()

    # CreditCard
    mycursor.execute("""
    CREATE TABLE CreditCard (
        CardID int NOT NULL AUTO_INCREMENT,
                    
        NameOnCard VARCHAR(20) NOT NULL,
        CardNumber VARCHAR(20) NOT NULL,
        CardSecurityCode VARCHAR(5) NOT NULL,
        CardExpirationMonth VARCHAR(5) NOT NULL,
        CardExpirationYear VARCHAR(5) NOT NULL,
                    
        PRIMARY KEY (CardID)
    )
    """)

    # Location
    mycursor.execute("""
    CREATE TABLE Location (
        LocationID int NOT NULL AUTO_INCREMENT,
                    
        BuildingNumber VARCHAR(20) NOT NULL,
        RoomNumber VARCHAR(20) NOT NULL,
                    
        PRIMARY KEY (LocationID)
    )
    """)

    # Account
    mycursor.execute("""
    CREATE TABLE Account (
        AccountID int NOT NULL AUTO_INCREMENT,
        CardID int NOT NULL,
                    
        Email VARCHAR(100) NOT NULL,
        Password VARCHAR(100) NOT NULL,
        Name VARCHAR(100) NOT NULL,
                    
        PRIMARY KEY (AccountID),
        FOREIGN KEY (CardID) REFERENCES CreditCard(CardID)
    )
    """)

    # Restaurant
    mycursor.execute("""
    CREATE TABLE Restaurant (
        RestaurantID int NOT NULL AUTO_INCREMENT,
        LocationID int NOT NULL,
                    
        Name VARCHAR(50) NOT NULL,
        Hours VARCHAR(50) NOT NULL,
        ImagePath VARCHAR(255) NOT NULL,  
        NumberReviews int NOT NULL,
        TotalReviewScores int NOT NULL,
                    
        PRIMARY KEY (RestaurantID),
        FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
    )
    """)

    # Food
    mycursor.execute("""
    CREATE TABLE Food (
        FoodID int NOT NULL AUTO_INCREMENT,
        RestaurantID int NOT NULL,
        
        Name VARCHAR(50) NOT NULL,
        Description VARCHAR(50),
        Price DECIMAL(10,2) NOT NULL,
        ImagePath VARCHAR(255) NOT NULL,             
        
        PRIMARY KEY (FoodID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    )
    """)

    # Order
    mycursor.execute("""
    CREATE TABLE Orders (
        OrderID int NOT NULL AUTO_INCREMENT,
        RestaurantID int NOT NULL,
        LocationID int NOT NULL,
        CustomerID int NOT NULL,
        
        OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        TotalAmount DECIMAL(10, 2) NOT NULL,
        
        PRIMARY KEY (OrderID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
        FOREIGN KEY (LocationID) REFERENCES Location(LocationID),
        FOREIGN KEY (CustomerID) REFERENCES Account(AccountID)
    )
    """)

    mycursor.close() # close cursor
    mydb.close() # close database

#createTables()

