import json
from pprint import pprint

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch

FROM_CITY = "LON"

flight_search = FlightSearch()
data_manager = DataManager()


def missing_iata():
    """Use this func if you have missing iata's in the google sheet. i only made this a function because i have limited api calls on sheety so i cant use it too much. sooooo use with caution
    """
    print(data_manager.sheet_data)
    for list in data_manager.sheet_data:
        city = list["city"]
        iata = flight_search.get_iatacode(city)
        if list["iataCode"] == "":
            list["iataCode"] = iata
            data_manager.update_sheet(column="iataCode",
                                      item=iata,
                                      id=list["id"])


# below is running thro all destinations in sheet_data (which is a local save of the google sheet) and checking if there is a cheaper price then the listed 'lowest price.' if there is it notifies you of the deal
for destination in data_manager.sheet_data:
    iata_code = destination["iataCode"]
    lowest_price = destination["lowestPrice"]

    if flight_search.search_flight(FROM_CITY, iata_code) is None:
        continue
    if flight_search.flight_data.price <= lowest_price:
        price = flight_search.flight_data.price
        origin_airport = flight_search.flight_data.origin_airport
        destination_airport = flight_search.flight_data.destination_airport

        print(
            f"\nDEAL FOUND!\nOrigin city: {origin_airport}\nDestination: {destination_airport}\nPrice: {price}\n"
        )

# im leaving the code here its supposed to notify you via sms but for reasons mentioned in previous lessons im not using that api.