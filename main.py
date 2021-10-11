import mysql.connector
from mysql.connector import Error
import pandas as pd
import queryCommands as qc
import time

from dotenv import load_dotenv
from os import getenv
load_dotenv() 
SQL_KEY = getenv("SQL")

import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

#Creates the database - only needs to be ran once :P

# def create_server_connection(host_name, user_name, user_password):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password
#         )
#         print("MySQL Database connection successful")
#     except Error as err:
#         print(f"Error: '{err}'")

#     return connection

# connection = create_server_connection("localhost", "root", SQL_KEY) 

# def create_database(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Database created successfully")
#     except Error as err:
#         print(f"Error: '{err}'")

# create_database_query = "CREATE DATABASE user_transaction_program"
# create_database(connection, create_database_query)


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("localhost", "root", SQL_KEY,"user_transaction_program") # Connect to the Database



def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit() 
        cursor.close() 
        return True

    except Error as err:
        cursor.close() 
        return False

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def menu():
    print("Welcome to Transaction Tracker!\n")
    print("Main Menu:")
    print("[C] - Create account")
    print("[A] - Access existing account")
    print("[Q] - Quit\n")
    while True:
        page = input("What would you like to do? ")
        if page in ["C","A","Q","c","a","q"]:
            break
    return page.lower()

def create_account():
    print("Create a new account.\n")
    username = input("Enter your username: ").lower()
    if execute_query(connection, qc.create_user_table(username)):
        print(f"New account succesfully created called {username}")
    else:
        print("That user already exists or there was an error.")
    print("Returning to menu ... ")


def checkTableExists(tablename):
    dbcur = connection.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False



def access_account():  
    exit = False
    userInput=""

    while exit == False:
        clearConsole()
        print("Access existing accounts.\n")
        username = input("Enter your username: ").lower()
        clearConsole()    
        if checkTableExists(username):
            print(f"Account found for [{username}]:")
            print("[V] - View all")
            print("[I] - Insert entry")
            print("[Q] - Quit and return to main menu\n")
            while True:
                userInput = input("What would you like to do: ")
                if userInput in ["V","I","Q","v","i","q"]:
                    break
        else:
            print(f"Account [{username}] does not exist or there was an error.")
            userInput = "q"
        
        if userInput == "q":
            print("Returning to main menu ... ")
            exit = True
        elif userInput == "v":
            results = qc.full_user_table(username)

            for result in results:
                print(result)
        elif userInput == "i":
            maxID = execute_query(connection,qc.get_max_ID(username))

            print (maxID)
            
            
            id = maxID+1
            print("Please enter a date in the format YYYY-MM-DD")
            date = input("Date: ")
            print("Please enter the category this transaction is in (ex: food,entertainement,rent)")
            category = input("Category: ").lower()
            print("Please enter the amount in $CAD")
            amount = input("Amount: ")
            print("Please enter the payment method used (ex: cash,MasterCard,cheque)")
            payment_method = input("Payment method: ").lower()

            if execute_query(connection, qc.insert(username,id,date,category,amount,payment_method)):
                print("Insert Success!")
            else:
                print("Insert failed or invalid inputs")
                print("Returning to main menu ... ")
                exit = True


def main ():
    exit = False
    
    while exit == False:
        clearConsole()
        userInput = menu()
        if userInput == "q":
            print("Quitting ... ")
            time.sleep(3)
            clearConsole()
            exit = True
        elif userInput == "c":
            create_account()
            time.sleep(3)
            clearConsole    ()
        elif userInput == "a":
            access_account()
            time.sleep(3)
            clearConsole()


main()