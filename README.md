#### Flight Tracker Twitter Bot

This is a Python script that fetches flight data from an XML feed and posts a tweet for flight arrivals and departures. The script also checks the difference between the scheduled and actual times for each flight.

##### Prerequisites
  - Python 3.x
  - Requests library
  - Tweepy library
  - Pytz library
  
##### Setup
1. Clone or download the repository.
2. Create a Twitter account for your bot if you haven't already.
3. Create a Twitter Developer account and create a new app to get your API keys and access tokens.
4. Create a new file named keys.py in the same directory as the script and add the following code, replacing the placeholders with your own API keys and access tokens:

```
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
```

##### Usage

To run the script, simply navigate to the directory where the script is located and run the command
`python flight_tracker.py`
The script will start fetching flight data from the XML feed and posting tweets for flight arrivals and departures.

##### Customization

You can customize the behavior of the script by modifying the following variables:

+ `flight_status`: A dictionary that keeps track of the flight status.
+ `tweeted_flights`: A set that keeps track of the flights that have been tweeted about.
+ `latest_tweet_time`: A variable that keeps track of the latest tweet time.
+ You can also customize the message format and hashtags of the tweet by modifying the text in the `api.update_status` method.

Live example: https://twitter.com/BGO_flights
