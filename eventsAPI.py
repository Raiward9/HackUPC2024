import requests
from datetime import datetime
from dataclasses import dataclass

uri = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=yhLUu4K12SkgG9JHcbG3qvrsx4WehgdU"

# Ticketmaster API key
API_KEY = 'yhLUu4K12SkgG9JHcbG3qvrsx4WehgdU'

# Base URL for Ticketmaster API
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/'

# Endpoint for searching events
SEARCH_EVENTS_ENDPOINT = 'events.json'

@dataclass
class Event:
    name: str
    type: str
    date: str
    time: str
    venue: str

def getEventsInfo(events:list[dict]):
    eventsInfo = []
    for event in events:
        name = event['name']
        type = event['classifications'][0]['segment']['name']
        date =  event['dates']['start']['localDate']
        time = event['dates']['start']['localTime']
        venue = event['_embedded']['venues'][0]['name']
        eventsInfo.append(Event(name,type,date,time,venue))
    
    return eventsInfo


def getActivitiesFromCityAndDate(cityName:str, dateIni:str, dateEnd:str):
    params = {
    'apikey': API_KEY,
    'city': cityName, 
    'startEndTime' : [dateIni,dateEnd],
    }
    response = requests.get(BASE_URL + SEARCH_EVENTS_ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        return getEventsInfo(data['_embedded']['events'])

    else: print("Error while making a request to api")


# ---------------- TESTING ----------------
#dateSt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  
#print(getActivitiesFromCityAndDate('Syracuse',dateSt))
