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

def doOneQueryPerInterest(depDate:datetime.datetime, retDate:datetime.datetime, city:str, preferences:list[str]) -> dict:
        resultPreferences = {}
        for preference in preferences:
            results = doQuery(depDate, retDate, city, preference)
            results = list(results)
            resultPreferences[preference] = results
            
        return resultPreferences

def doQuery(depDate:datetime.datetime, retDate:datetime.datetime, city:str, preference:str) -> Cursor:
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
    
    if not preference in interests:
        print("Invalid preference", preference, ", not in", interests)
        return None
        
    
    query = {"Departure Date": {"$lt": retDate.isoformat()},
             "Return Date": {"$gt":depDate.isoformat()},
             "Arrival City":city,
             "Activities":preference}
    
    return collection.find(query)

def addUser(name:str, depDate:datetime.datetime, retDate:datetime.datetime, depCity:str, arrCity:str, activities:list[str]):
    global dbClient
    ntries = 0
    while (dbClient == None and ntries < 5):
        initDbClient()
        ntries += 1
        
    if ntries == 5:
        raise Exception("Failed connection")
    
    db = dbClient['hackupc_travel']
    collection = db['travel_info']
    
    if not depCity in cities:
        print("Invalid city", depCity, ", not in", cities)
        return None
    
    if not arrCity in cities:
        print("Invalid city", arrCity, ", not in", cities)
        return None
    
    for preference in activities:
        if not preference in interests:
            print("Invalid preference", preference, ", not in", interests)
            return None
    
    individual = {
        "Traveller Name": name,
        "Departure Date": depDate.isoformat(),
        "Return Date": retDate.isoformat(),
        "Departure City": depCity,
        "Arrival City": arrCity,
        "Activities": activities}
    
    try:
        collection.insert_one(individual)
    except Exception as error:
        print("An exception occurred:", error)
    