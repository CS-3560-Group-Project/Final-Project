
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
    CardID int NOT NULL,
    AccountID int NOT NULL,
    NameOnCard VARCHAR(20) NOT NULL,
    CardNumber VARCHAR(20) NOT NULL,
    CardSecurityCode VARCHAR(5) NOT NULL,
    CardExpirationMonth VARCHAR(5) NOT NULL,
    CardExpirationYear VARCHAR(5) NOT NULL,
    PRIMARY KEY (CardID),
    FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
)
""")

# Account
mycursor.execute("""
CREATE TABLE Account (
    AccountID int NOT NULL,
    LocationID int NOT NULL,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    PRIMARY KEY (AccountID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
)
""")

# Location
mycursor.execute("""
CREATE TABLE Location (
    LocationID int NOT NULL,
    BuildingNumber VARCHAR(20) NOT NULL,
    RoomNumber VARCHAR(20) NOT NULL,
    PRIMARY KEY (LocationID),
)
""")

# Restaurant
mycursor.execute("""
CREATE TABLE Restaurant (
    RestaurantID int NOT NULL,
    LocationID int NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Hours VARCHAR(50) NOT NULL,
    PRIMARY KEY (RestaurantID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
)
""")

mycursor.close() # close cursor
mydb.close() # close database