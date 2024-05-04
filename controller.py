import datetime
from dataclasses import dataclass
from databaseController import initDbClient, doOneQueryPerInterest
from eventsAPI import getActivitiesFromCityAndDate

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

activityToCategory = {'Art Exhibitions':'Art and Culture', 
            'Beach Volleyball':'Sports and Fitness',
            'Concerts':'Music',
            'Cooking Classes':'Gastronomy',
            'Cultural Festivals':'Art and Culture',
            'Dancing Classes':'Music',
            'Escape Rooms':'Miscellaneous',
            'Food Tours':'Gastronomy',
            'Football Matches':'Sports and Fitness',
            'Group Cycling Tours':'Sports and Fitness',
            'Hiking Excursions':'Adventure',
            'Hot Air Balloon Rides':'Adventure',
            'Karaoke Nights':'Music',
            'Kayaking':'Sports and Fitness',
            'Pub Crawls':'Music',
            'River Cruises':'City Exploration',
            'Rock Climbing':'Sports and Fitness',
            'Scavenger Hunts':'Miscellaneous',
            'Segway Tours':'City Exploration',
            'Sightseeing Tours': 'City Exploration',
            'Snorkeling Tours': 'Adventure',
            'Theater Performances':'Art and Culture',
            'Theme Parks':'Miscellaneous',
            'Wine Tasting':'Gastronomy',
            'Zip Line Adventures':'Adventure'}

def getEvents(depDate:datetime.datetime, retDate:datetime.datetime, city:str, activities:list[str]) -> dict:
    initDbClient()
    peoplePerActivity = doOneQueryPerInterest(depDate, retDate, city, activities)
    events = getActivitiesFromCityAndDate(city, depDate, retDate)
    
    result = []
    eventsChosen = []
    for activitat, persones in peoplePerActivity.items():

        category = activityToCategory[activitat]
        desiredEvent = None
        
        for event in events:
            if event.classification == category:
                desiredEvent = event
                break

        nomsPersones = []
        for persona in persones:
            nomsPersones.append(persona['Traveller Name'])

        if len(nomsPersones) > 10: 
            nomsPersones = nomsPersones[:10]
        

        if desiredEvent != None and not desiredEvent in eventsChosen:
            result.append((desiredEvent, nomsPersones))
            eventsChosen.append(desiredEvent)

    print(result)
        
    return result
