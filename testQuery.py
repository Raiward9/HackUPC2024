from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime

def getDbClient() -> MongoClient:
    uri = "mongodb+srv://sergimartinezpamias:FwIFc70b407VBCuw@smp.16uhelv.mongodb.net/?retryWrites=true&w=majority&appName=SMP"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None


def doQuery(collection, depDate:datetime.datetime, retDate:datetime.datetime):
    query = {"Departure Date": {"$lt": retDate.isoformat()}, "Return Date": {"$gt":depDate.isoformat()}}
    
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

def main():
    client = getDbClient()
    if client == None:
        print("Connection failed!")
        return
    
    db = client['hackupc_travel']
    collection = db['travel_info']
    
    depDate = askForDate("Please enter an arrival date (YYYY-MM-DD): ")
    retDate = askForDate("Please enter a return date (YYYY-MM-DD): ")
        
    results = doQuery(collection, depDate, retDate)
    
    for res in results:
        print(res['Departure Date'])
            
if __name__ == "__main__":
    main()
    
    
