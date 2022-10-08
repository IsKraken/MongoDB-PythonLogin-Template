from pymongo import MongoClient
from colorama import Fore, Back
from os import system, environ
import random
import time

my_secret = '' # Provide the mongodb atlas url to connect python to mongodb using pymongo

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
def get_database():
    CONNECTION_STRING = my_secret
    client = MongoClient(CONNECTION_STRING)
    return client['userinfo']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
  #This will auto get the name no need to change
    dbname = get_database()

# Creates a one time and UNIQUE ID for the user
def user_f_create_UID():
    ID_NUMBER = random.randint(10000000000, 99999999999)
    user_created_UID = f'UID_BETA_{ID_NUMBER}'
    user_f_create_data_username(user_created_UID)

# Will confirm that the TABLE/Collection Exists, Will automatically make one if needed
collect_collection = dbname["login"]

# The process it takes for the username
def user_f_create_data_username(user_created_UID):
    system('clear')
    collect_username = input('USERNAME : ')
    # Checks to make sure the length of username is a right ammount.
    collect_username_length = len(collect_username)
    if collect_username_length <= 3:
        print(
            Back.RED +
            f'Must contain 4 or more chrachters, Not ({collect_username_length})',
            Back.RESET)
        time.sleep(1.5)
        user_f_create_data_username(user_created_UID)
    username_check = collect_collection.find(
        {"user": collect_username.lower()})
    for value in username_check:
        # This is set for one time usernames, No two people can be one username
        print(Back.RED +
              '⚠️  The username you have attempted is currently owned...')
        print(Back.RED + 'Returning to username phase!', Back.RESET)
        time.sleep(2)
        system('clear')
        user_f_create_data_username(user_created_UID)
    else:
      # This creates the data for the username (Automatically puts it to lower for finding reasons.)
        user_created_data = ({"user": collect_username.lower()})
        user_created_data.update({"user_original_format": collect_username})
        user_f_create_data_password(user_created_data, user_created_UID)

# Creates data for password
def user_f_create_data_password(user_created_data, user_created_UID):
    collect_password = input('PASSWORD : ')
    collect_password_length = len(collect_password)
    if collect_password_length<5:
      # Makes sure password is above 6 or more charachters
      print(Back.RED + f'⚠️  Warning! : Your password is only {collect_password_length}, please change that to 6 or more!')
      time.sleep(2)
      user_f_create_data_password(user_created_data, user_created_UID)
    user_created_data.update({"password": collect_password})
    user_f_create_data_name(user_created_data, user_created_UID)

# Takes data from name and imports it.
def user_f_create_data_name(user_created_data, user_created_UID):
    collect_name = input('NAME : ')
    user_created_data.update({"name": collect_name})
    user_f_create_data_info(user_created_data, user_created_UID)


def user_f_create_data_info(user_created_data, user_created_UID):
  # I was using this for another field, but its now for The Unique, User ID
    user_created_data.update({"_id": user_created_UID})
    user_f_create_check_UID(user_created_data, user_created_UID)

#Checks if the UNIQUE ID is not so UNIQUE and regenerates it if taken.
def user_f_create_check_UID(user_created_data, user_created_UID):
    id_check = collect_collection.find({"_id": user_created_UID})
    for item in id_check:
        if item["_id"] == user_created_UID:
            ID_NUMBER = random.randint(10000000000, 99999999999)
            user_created_UID = f'UID_BETA_{ID_NUMBER}'
            user_created_data.update({"_id": user_created_UID})
            print(Fore.LIGHTGREEN_EX + 'Saved!', Fore.RESET)
            user_f_create_check_UID(user_created_data, user_created_UID)
    else:
      # Tells client if it has been created succesfully!
        collect_collection.insert_one(user_created_data)
        print('Sucess')
        time.sleep(1.1)
        system('clear')
        user_f_act()

# Whole login process not as organized as creation
def user_f_login():
    collect_username = input('What is your username: ')
    collect_password = input('What is your password: ')
    lower_username = collect_username.lower()
  # Making sure there is a user with the name inputted
    check_username_exists = collect_collection.find_one({"user": lower_username})
    if check_username_exists == None:
      print(Back.RED + '⚠️  Warning!: Please re-check your response as it may not exist', Back.RESET)
      time.sleep(3)
      system('clear')
      user_f_login()
    elif check_username_exists["user"] == lower_username:
      if check_username_exists["password"] == collect_password:
        print(f'Hello, {check_username_exists["name"]}. You have been granted in!')
      else:
        # If the password isnt existent try again!
        print(Back.RED + '⚠️  Warning!: Failed password', Back.RESET)
        time.sleep(1)
        system('clear')
        user_f_login()

#Basic selection menu for login or creation.
def user_f_act():
    print(Fore.LIGHTBLUE_EX, end = '')
    user_f_response = input('Login[1] or Create[2] ~ ')
    if user_f_response == '1':
        system('clear')
        user_f_login()
    elif user_f_response == '2':
        system('clear')
        user_f_create_UID()
    else:
        print(Back.RED + '⚠️  Invalid command', Back.RESET)
        time.sleep(1.1)
        system('clear')
        user_f_act()

user_f_act()
