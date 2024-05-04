import requests
from random import shuffle
from datetime import datetime
from dataclasses import dataclass
from huggingface_hub.inference_api import InferenceApi

# Hugging face
API_TOKEN_HUGGINGFACE = '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'
inference = None
classifications = ['Art and Culture', 'Music', 'Adventure', 'Sports and Fitness', 'Gastronomy', 'City Exploration', 'Escape Rooms', 'Scavenger Hunts', 'Theme Parks']

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
    classification: str

def getEventsInfo(events:list[dict]):
    print(len(events))
    shuffle(events)
    eventsInfo:list[Event] = []
    found:set = set({})
    names = set({})
    nevents = 0
    for event in events:
        try:
            name = event['name']
            if name in names:
                continue
            type = event['classifications'][0]['segment']['name']
            date =  event['dates']['start']['localDate']
            time = event['dates']['start']['localTime']
            venue = event['_embedded']['venues'][0]['name']
        except:
            continue
        nevents += 1
        names.add(name)
        eventsInfo.append(Event(name,type,date,time,venue,""))
        classifyEvent(eventsInfo[-1])
        found.add(eventsInfo[-1].classification)
        if len(found) == 4 or nevents == 20:
            break
    
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
        try:
            return getEventsInfo(data['_embedded']['events'])
        except:
            return []

    else: print("Error while making a request to api")


def classifyEvent(e: Event):
    global inference
    if inference == None:
        inference = InferenceApi(repo_id="typeform/distilbert-base-uncased-mnli", token=API_TOKEN_HUGGINGFACE)
        
    inputs = "Classify the following activity: \""+ e.name + "\" in venue:\"" + e.venue + "\" of type: \"" + e.type + "\""
    params = {"candidate_labels":classifications}
    out = inference(inputs, params)
    e.classification = out['labels'][0]
    if e.classification in ['Escape Rooms', 'Scavenger Hunts', 'Theme Parks']:
        e.classification = 'Miscellaneous'
    
    
    
    

# ---------------- TESTING ----------------
#dateSt = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  
#print(getActivitiesFromCityAndDate('Syracuse',dateSt))
