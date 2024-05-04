import datetime
from databaseController import initDbClient, doOneQueryPerInterest
from eventsAPI import getActivitiesFromCityAndDate

def getEvents(depDate:datetime.datetime, retDate:datetime.datetime, city:str, activities:list[str]) -> dict:
    initDbClient()
    peoplePerActivity = doOneQueryPerInterest(depDate, retDate, city, activities)
    events = getActivitiesFromCityAndDate(cityName=city, depDate, retDate)
    
