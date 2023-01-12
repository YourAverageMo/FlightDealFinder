import json
import os
from datetime import datetime, timedelta

import requests
from dotenv import find_dotenv, load_dotenv

from flight_data import FlightData

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TEQUILA_BASE_URL = "https://api.tequila.kiwi.com/"
TEQUILA_SEARCH_QUERY_URL = "locations/query"
TEQUILA_FLIGHT_SEARCH_URL = "search"
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_HEADER = {"apikey": TEQUILA_API_KEY}


class FlightSearch:

    def __init__(self):
        pass

    def get_iatacode(self, city_name):
        """fetch iatacode for city_name using tequilla search query api

        Args:
            city_name (str): city name to search for in tequillas api

        Returns:
            str: the iatacode for said city_name
        """
        tequila_params = {
            "term": city_name,
            "location_types": "airport",
            "limit": 1,
            "active_only": "true"
        }
        tequila_iata_response = requests.get(
            url=f"{TEQUILA_BASE_URL}{TEQUILA_SEARCH_QUERY_URL}",
            params=tequila_params,
            headers=TEQUILA_HEADER)

        search_query_data = tequila_iata_response.json()

        # temp saving response locally for ref. id prefer to keep this stuff
        with open("temp_data.json", mode="w") as file:
            json.dump(search_query_data, file)

        return search_query_data["locations"][0]["city"]["code"]

    def search_flight(self, from_city, dest_city):
        """fetches the cheapest flight and relevant data from {from_city} to {dest_city}. search crit {departure: today-180 days from now, trip length: 7-28 days, roundtrip direct flights only, currency: usd)\nThen creates a new flight_data class instance to store said data. data can be accessed via self.flight_data

        Args:
            from_city (str): departure city
            dest_city (str): destination city
        """

        start_date = datetime.today().strftime("%d/%m/%Y")
        end_date = (datetime.today() +
                    timedelta(days=180)).strftime("%d/%m/%Y")

        tequila_search_params = {
            "fly_from": from_city,
            "fly_to": dest_city,
            "date_from": start_date,
            "date_to": end_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "limit": 1,
            "max_stopovers": 0,
            "flight_type": "round",
            "curr": "USD",
        }
        tequila_search_response = requests.get(
            url=f"{TEQUILA_BASE_URL}{TEQUILA_FLIGHT_SEARCH_URL}",
            params=tequila_search_params,
            headers=TEQUILA_HEADER)
        try:
            flight_search_data = tequila_search_response.json()
        except:
            print(flight_search_data)
            return None
        else:
            print(f"downloaded flight search data successfully")
            with open("temp_flight_data.json", mode="w") as file:
                json.dump(flight_search_data, file)

            self.flight_data = FlightData(
                price=flight_search_data["data"][0]["price"],
                origin_city=flight_search_data["data"][0]["route"][0]
                ["cityFrom"],
                origin_airport=flight_search_data["data"][0]["route"][0]
                ["flyFrom"],
                destination_city=flight_search_data["data"][0]["route"][0]
                ["cityTo"],
                destination_airport=flight_search_data["data"][0]["route"][0]
                ["flyTo"],
            )
            return self.flight_data