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
    activitiesToEvents = {}
    for activitat, persones in peoplePerActivity.items():

        category = activityToCategory[activitat]
        desiredEvent = None
        
        for event in events:
            if event.classification == category:
                desiredEvent = event
                if desiredEvent in activitiesToEvents:
                    activitiesToEvents[desiredEvent.name].append(activitat)
                else:
                    activitiesToEvents[desiredEvent.name] = [activitat]

                break

        nomsPersones = []
        for persona in persones:
            nomsPersones.append(persona['Traveller Name'])

        if len(nomsPersones) > 10: 
            nomsPersones = nomsPersones[:10]
        

        if desiredEvent != None and not desiredEvent.name in activitiesToEvents:
            result.append((desiredEvent, nomsPersones, activitiesToEvents[desiredEvent.name]))

    print(result)
        
    return result


# --------------------------------------------------- TEST --------------------------------------------------------------------------

cities = ['Amsterdam', 'Barcelona', 'Berlin', 'Brussels', 'Budapest', 'Dublin', 'Florence', 'Lisbon', 'London', 'Madrid', 'Milan', 'Munich', 'Paris', 'Prague', 'Rome', 'Vienna', 'Zurich']
interests = ['Art Exhibitions', 'Beach Volleyball', 'Concerts', 'Cooking Classes', 'Cultural Festivals', 'Dancing Classes', 'Escape Rooms', 'Food Tours', 'Football Matches', 'Group Cycling Tours', 'Hiking Excursions', 'Hot Air Balloon Rides', 'Karaoke Nights', 'Kayaking', 'Pub Crawls', 'River Cruises', 'Rock Climbing', 'Scavenger Hunts', 'Segway Tours', 'Sightseeing Tours', 'Snorkeling Tours', 'Theater Performances', 'Theme Parks', 'Wine Tasting', 'Zip Line Adventures']

def askForDate(prompt:str) -> datetime.datetime:
    date_input = input(prompt)

    try:
        # Parse the input string into a datetime object
        user_date = datetime.datetime.strptime(date_input, "%Y-%m-%d")
        print("You entered:", user_date)
        return user_date
    except ValueError:
        print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")
        return askForDate(prompt)

def askForCity(prompt:str) -> str:
    city_input = input(prompt + "Choose from: " + str(cities) + "\n")
    
    if not city_input in cities:
        print("City not available")
        return askForCity(prompt)
    else:
        return city_input
    
def askForInterests(prompt:str)->list[str]:
    retlist = []
    print(prompt)
    while (input("Current interests: " + str(retlist) + ";\nAny more interests [y/n]") != "n"):
        int_input = input(prompt + "Choose from: " + str(interests) + "\n")    
        if not int_input in interests:
            print("Interest not available")
        else:
            retlist.append(int_input)
        
    return retlist
            

def main():
    
    depDate = askForDate("Please enter an arrival date (YYYY-MM-DD): ")
    retDate = askForDate("Please enter a return date (YYYY-MM-DD): ")
    city = askForCity("Please enter arrival city; ")
    profile = askForInterests("Please enter your interests; ")
        
    results = getEvents(depDate, retDate, city, profile)

    for res in results:
        print(res)

            
if __name__ == "__main__":
    main()
    