# IMPORTANT this code is now hosted on repl at the below link. just hit run and you can automatically save customer data on the spreadsheet :D
# https://replit.com/@UsameYilmaz/CustomerAcquistion#main.py

import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SHEETY_POST_ENDPOINT = "https://api.sheety.co/fc306af276b4dd401b5dea17312a8f52/flightDeals/users"
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")
SHEETY_HEADER = {"Authorization": SHEETY_TOKEN}


print(
    "Welcome to the F(l)ight Club!\nWhere we find the best deals on airline tickets around the world.\n"
)
not_signed_up = True
while not_signed_up:
    first_name = input("To sign up please enter your First Name.\n")
    last_name = input("\nAnd what is your last name?.\n")
    email = input("\nWhat is your email?.\n")
    email_verification = input(
        "\nplease verify your email by typing it again.\n")

    if email == email_verification:
        sheety_users_json = {
            "user": {
                "firstName": first_name.title(),
                "lastName": last_name.title(),
                "email": email.lower(),
            }
        }
        response = requests.post(url=f"{SHEETY_POST_ENDPOINT}",
                                headers=SHEETY_HEADER,
                                json=sheety_users_json)
        data = response.json()
        if "errors" not in data:
            print("\nSuccess! Welcome to the F(l)ight Club!")
            not_signed_up = False
        else:
            print(data)
    else:
        print(
            "\nsorry that didn't match please go through the sign-up process one more time.\n"
        )
