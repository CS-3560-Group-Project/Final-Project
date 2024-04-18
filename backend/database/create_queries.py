
# Pip
# python -m pip install mysql-connector-python

# Imports
import mysql.connector

HOST = "localhost"
USER = "tannaz"
PASSWORD = "damavandi"
DATABASE_NAME = "FoodDelivery"

##### CREATE DATABASE #####

# Connect to the databse
mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)

# Create a database
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS FoodDelivery")
mycursor.close() # close cursor
mydb.close() # close database

##### CREATE TABLES #####

# Conntect to the database
mydb = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME)

# CreditCard
mycursor.execute("""
CREATE TABLE CreditCard (
    CardID int NOT NULL AUTO_INCREMENT,
                 
    NameOnCard VARCHAR(20) NOT NULL,
    CardNumber VARCHAR(20) NOT NULL,
    CardSecurityCode VARCHAR(5) NOT NULL,
    CardExpirationMonth VARCHAR(5) NOT NULL,
    CardExpirationYear VARCHAR(5) NOT NULL,
                 
    PRIMARY KEY (CardID),
)
""")

# Account
mycursor.execute("""
CREATE TABLE Account (
    AccountID int NOT NULL AUTO_INCREMENT,
    LocationID int NOT NULL,
    CardID int NOT NULL,
                 
    Username VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
                 
    PRIMARY KEY (AccountID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
    FOREIGN KEY (CardID) REFERENCES CreditCard(CardID)
)
""")

# Location
mycursor.execute("""
CREATE TABLE Location (
    LocationID int NOT NULL AUTO_INCREMENT,
                 
    BuildingNumber VARCHAR(20) NOT NULL,
    RoomNumber VARCHAR(20) NOT NULL,
                 
    PRIMARY KEY (LocationID),
)
""")

# Restaurant
mycursor.execute("""
CREATE TABLE Restaurant (
    RestaurantID int NOT NULL AUTO_INCREMENT,
    LocationID int NOT NULL,
                 
    Name VARCHAR(50) NOT NULL,
    Hours VARCHAR(50) NOT NULL,
                 
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
    
    PRIMARY KEY (FoodID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
)
""")

# Order
mycursor.execute("""
CREATE TABLE Order (
    OrderID int NOT NULL AUTO_INCREMENT,
    RestaurantID int NOT NULL,
    CustomerID int NOT NULL,
    
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    
    PRIMARY KEY (OrderID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
)
""")

# Review
mycursor.execute("""
CREATE TABLE Review (
    ReviewID int NOT NULL AUTO_INCREMENT,
    RestaurantID int NOT NULL,
    CustomerID int NOT NULL,
    
    Rating int NOT NULL,
    Comment VARCHAR(250),
    ReviewDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (ReviewID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
)
""")

mycursor.close() # close cursor
mydb.close() # close database