import requests
from datetime import datetime

uri = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=yhLUu4K12SkgG9JHcbG3qvrsx4WehgdU"

# Your Ticketmaster API key
API_KEY = 'yhLUu4K12SkgG9JHcbG3qvrsx4WehgdU'

# Base URL for Ticketmaster API
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/'

# Endpoint for searching events
SEARCH_EVENTS_ENDPOINT = 'events.json'

def showEventsInfo(events):
    for event in events:
        print("Name:", event['name'])
        print("Date:", event['dates']['start']['localDate'])
        print("Time:", event['dates']['start']['localTime'])
        print("Type:", event['classifications'][0]['segment']['name'])
        print("Venue:", event['_embedded']['venues'][0]['name'])
        print('----------------------------------------------')


def getActivitiesFromCityAndDate(cityName,date):
    params = {
    'apikey': API_KEY,
    'city': cityName, 
    'startEndTime' : [date,date],
    }
    response = requests.get(BASE_URL + SEARCH_EVENTS_ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        showEventsInfo(data['_embedded']['events'])

    else: print("Error while making a request to api")

dateSt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  

# testing
getActivitiesFromCityAndDate('Syracuse',dateSt)
