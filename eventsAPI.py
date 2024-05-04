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
    pageLink: str
    imageURL: str
    date: str
    time: str
    venue: str
    classification: str

# returns the biggest image (width*height) in the list
def getMainImage(images:list):
    biggestSize = 0
    bestImage = ''
    for image in images:
        size = int(image['width'])*int(image['height'])
        if size > biggestSize: 
            bestImage = image
            biggestSize = size
    
    return bestImage


def getEventsInfo(events:list[Event]):
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
            pageLink = event['url']
            date =  event['dates']['start']['localDate']
            time = event['dates']['start']['localTime']
            venue = event['_embedded']['venues'][0]['name']
            images = event['images']
            image = getMainImage(images)['url']
        except:
            continue
        nevents += 1
        names.add(name)
        eventsInfo.append(Event(name,type,pageLink,image,date,time,venue,""))
        classifyEvent(eventsInfo[-1])
        found.add(eventsInfo[-1].classification)
        if len(found) == 4 or nevents == 20:
            break
    
    return eventsInfo


def getActivitiesFromCityAndDate(cityName:str, dateIni:datetime, dateEnd:datetime):
    dateIni = dateIni.strftime('%Y-%m-%dT%H:%M:%SZ')
    dateEnd = dateEnd.strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
    'apikey': API_KEY,
    'city': cityName, 
    'startDateTime': dateIni,
    'endDateTime': dateEnd,
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
#dateSt = datetime.now()
#dateEnd = datetime(2024,5,25)
#lst = getActivitiesFromCityAndDate('Syracuse',dateSt,dateEnd)
#for elem in lst: 
#    print(elem)
#    print('----------------')
#print(len(lst))
#lst2 = list(filter(lambda elem: elem.classification == "Miscellaneous",lst))
#print(len(lst2))
