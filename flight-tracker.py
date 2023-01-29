import xml.etree.ElementTree as ET
import requests
import tweepy
import time
import keys
from datetime import datetime
from pytz import timezone

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    keys.api_key, keys.api_secret, keys.access_token, keys.access_token_secret
)
api = tweepy.API(auth)

# Keep track of the flight status
flight_status = {}

# Keep track of the flights that have been tweeted about
tweeted_flights = set()

# Initialize the latest tweet time to the current time
latest_tweet_time = datetime.now()

while True:
    # Fetch the XML data feed from the URL
    response = requests.get(
        "https://flydata.avinor.no/XmlFeed.asp?TimeFrom=1&TimeTo=1&airport=BGO"
    )
    xml_data = response.text

    # Parse the XML data feed
    root = ET.fromstring(xml_data)

    # Iterate through the flights in the data feed
    for flight in root.findall("./flights/flight"):
        flight_number = flight.find("flight_id").text
        status_element = flight.find("status")
        if status_element is not None:
            arr_dep = status_element.attrib["code"]
            if "time" in status_element.attrib:
                actual_time = status_element.attrib["time"]
            if arr_dep == "A":
                # Convert the schedule time to local time in Bergen
                actual_time = actual_time.rstrip("Z")
                actual_time_bergen = (
                    datetime.strptime(actual_time, "%Y-%m-%dT%H:%M:%S")
                    .replace(tzinfo=timezone("UTC"))
                    .astimezone(timezone("Europe/Oslo"))
                )
                print(
                    f"Flight {flight_number} has arrived at {actual_time_bergen.strftime('%H:%M:%S')}"
                )
                if flight_number not in flight_status or flight_status[flight_number]["arr_dep"] != arr_dep or flight_status[flight_number]["time"] != actual_time:
                    if flight_number not in tweeted_flights:
                        try:
                            api.update_status(
                                f"✈️Flight Alert: Flight {flight_number} has arrived at {actual_time_bergen.strftime('%H:%M:%S')}\n\n#BergenAirport #Aviation #Travel #BGO"
                            )
                            tweeted_flights.add(flight_number)
                        except Exception as e:
                            print(f"Error sending tweet: {e}")
            elif arr_dep == "D":
                # Convert the schedule time to local time in Bergen
                actual_time = actual_time.rstrip("Z")
                actual_time_bergen = (
                    datetime.strptime(actual_time, "%Y-%m-%dT%H:%M:%S")
                    .replace(tzinfo=timezone("UTC"))
                    .astimezone(timezone("Europe/Oslo"))
                )
                print(
                    f"Flight {flight_number} has departed at {actual_time_bergen.strftime('%H:%M:%S')}"
                )
                if flight_number not in flight_status or flight_status[flight_number]["arr_dep"] != arr_dep or flight_status[flight_number]["time"] != actual_time:
                    if flight_number not in tweeted_flights:
                        try:
                            api.update_status(
                            f"✈️Flight Alert: Flight {flight_number} has departed at {actual_time_bergen.strftime('%H:%M:%S')}\n\n#BergenAirport #Aviation #Travel #BGO"
                            )
                            tweeted_flights.add(flight_number)
                        except Exception as e:
                            print(f"Error sending tweet: {e}")
    # Sleep for 3 minutes before fetching the next data feed
    time.sleep(180)
