import json
import os

import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SHEETY_POST_ENDPOINT = "https://api.sheety.co/fc306af276b4dd401b5dea17312a8f52/flightDeals/prices"
SHEETY_PUT_ENDPOINT = "https://api.sheety.co/fc306af276b4dd401b5dea17312a8f52/flightDeals/prices/"
SHEETY_TOKEN = os.getenv("SHEETY_TOKEN")
SHEETY_HEADER = {"Authorization": SHEETY_TOKEN}


class DataManager:

    def __init__(self):
        """On init open local version of the google doc; if it doesnt exist it fetches a new copy of the doc, and saves it as sheet_data.
        """
        try:
            with open("flight_deals_sheet.json", mode="r") as file:
                self.sheet_data = json.load(file)["prices"]
        except FileNotFoundError:
            self.get_sheety()
            with open("flight_deals_sheet.json", mode="r") as file:
                self.sheet_data = json.load(file)["prices"]

    def get_sheety(self):
        """uses sheety api to .get flight deals google sheet info

        Returns:
            ./flight_deals_sheet.json: json file of said google sheet saved to root
        """
        response = requests.get(url=f"{SHEETY_POST_ENDPOINT}",
                                headers=SHEETY_HEADER)
        data = response.json()
        with open("flight_deals_sheet.json", mode="w") as file:
            return json.dump(data, file)

    def update_sheet(self, column, item, id):
        """used to write to the online copy of sheet_data. use with caution since i have limited api calls

        Args:
            column (str): column you want to update for row no. {id}
            item (any): the value you want to write in said column in row no. {id}
            id (int): the row number to be passed
        """
        sheety_json = {
            "price": {
                column: item,
            }
        }
        response = requests.put(url=f"{SHEETY_PUT_ENDPOINT}{id}",
                                headers=SHEETY_HEADER,
                                json=sheety_json)
        data = response.json()
        if "errors" not in data:
            print(
                f"uploaded {item} as {column} in row # {id}  data successfully"
            )
        else:
            print(data)
