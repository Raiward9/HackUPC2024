from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.cursor import Cursor
import datetime

cities = ['Amsterdam', 'Barcelona', 'Berlin', 'Brussels', 'Budapest', 'Dublin', 'Florence', 'Lisbon', 'London', 'Madrid', 'Milan', 'Munich', 'Paris', 'Prague', 'Rome', 'Vienna', 'Zurich']
interests = ['Art Exhibitions', 'Beach Volleyball', 'Concerts', 'Cooking Classes', 'Cultural Festivals', 'Dancing Classes', 'Escape Rooms', 'Food Tours', 'Football Matches', 'Group Cycling Tours', 'Hiking Excursions', 'Hot Air Balloon Rides', 'Karaoke Nights', 'Kayaking', 'Pub Crawls', 'River Cruises', 'Rock Climbing', 'Scavenger Hunts', 'Segway Tours', 'Sightseeing Tours', 'Snorkeling Tours', 'Theater Performances', 'Theme Parks', 'Wine Tasting', 'Zip Line Adventures']

DEBUG = False
dbClient = None

def initDbClient():
    uri = "mongodb+srv://sergimartinezpamias:FwIFc70b407VBCuw@smp.16uhelv.mongodb.net/?retryWrites=true&w=majority&appName=SMP"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        if DEBUG: print("Pinged your deployment. You successfully connected to MongoDB!")
        global dbClient
        dbClient = client
    except Exception as e:
        print(e)
        return None


def doQuery(depDate:datetime.datetime, retDate:datetime.datetime, city:str, preferences:list[str]) -> Cursor:
    global dbClient
    ntries = 0
    while (dbClient == None and ntries < 5):
        initDbClient()
        ntries += 1
        
    if ntries == 5:
        raise Exception("Failed connection")
    
    db = dbClient['hackupc_travel']
    collection = db['travel_info']
    
    if not city in cities:
        print("Invalid city", city, ", not in", cities)
        return None
    
    for i in preferences:
        if not i in interests:
            print("Invalid preference", i, ", not in", interests)
            return None
        
    
    query = {"Departure Date": {"$lt": retDate.isoformat()},
             "Return Date": {"$gt":depDate.isoformat()},
             "Arrival City":city,
             "Activities":{"$in":interests}}
    
    return collection.find(query)

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
        
    results = doQuery(depDate, retDate, city, profile)
    
    for res in results:
        print(res)
            
if __name__ == "__main__":
    main()
    
    
