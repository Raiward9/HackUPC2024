from taipy import Gui
from datetime import datetime
import taipy.gui.builder as tgb
from taipy.gui import State
import taipy as tp
from taipy.gui import navigate


from controller import getEvents

cities = ['Amsterdam', 'Barcelona', 'Berlin', 'Brussels', 'Budapest', 'Dublin', 'Florence', 'Lisbon', 'London', 'Madrid', 'Milan', 'Munich', 'Paris', 'Prague', 'Rome', 'Vienna', 'Zurich']
date_init = datetime.now()
date_end = datetime.now()


departure = ""
arrival = ""

categoryToActivity = {'Art and Culture': ['Art Exhibitions', 'Cultural Festivals', 'Theater Performances'], 
                      'Music': ['Concerts', 'Dancing Classes', 'Karaoke Nights', 'Pub Crawls'], 
                      'Adventure': ['Hiking Excursions', 'Hot Air Balloon Rides', 'Snorkeling Tours', 'Zip Line Adventures'], 
                      'Sports and Fitness': ['Beach Volleyball', 'Football Matches', 'Group Cycling Tours', 'Kayaking', 'Rock Climbing'], 
                      'Gastronomy': ['Cooking Classes', 'Food Tours', 'Wine Tasting'], 
                      'City Exploration': ['River Cruises', 'Segway Tours', 'Sightseeing Tours'], 
                      'Miscellaneous': ['Escape Rooms', 'Scavenger Hunts', 'Theme Parks']}
categories = list(categoryToActivity.keys())
activities = []
selected_activities = []
selected_categories = []
events = []

init = True
start_again = False
all_fields = False

def change_init(state):
    state.init = False
    state.start_again = True
    state.events = getEvents(state.date_init, state.date_end, state.arrival, state.selected_activities)
    #state.events = getEvents(datetime(2024,6,4), datetime(2024,7,5), "Barcelona", ["Concerts"])
    while state.events == []:
        True
    print("Events: ", state.events)
    navigate(state, "feed")
    print("Events 3: ", state.events)
def default_values(state):
    state.init = True
    state.start_again = False
    state.departure = ""
    state.arrival = ""
    state.activities = []
    state.selected_activities = []
    state.selected_categories = []
    state.events = []
    navigate(state, "/")

def all_fields_filled(state):
    return state.departure != "" and state.arrival != "" and state.selected_categories != [] and state.selected_activities != []

def on_change(state, var_name: str, value: any):
    state.all_fields = all_fields_filled(state)
    if var_name == "departure":
        state.departure = value
    elif var_name == "arrival":
        state.arrival = value
    elif var_name == "selected_categories":
        state.selected_categories = value
        state.activities = []
        for e in state.selected_categories:
            for a in categoryToActivity[e]:
                state.activities.append(a)
    elif var_name == "selected_activities":
        state.selected_activities = value



with tgb.Page(on_refresh=default_values) as root_page:
    with tgb.part(render = "{init}"):
        tgb.text(value="# Welcome Traveler", mode="md", color="primary", align="center")
        with tgb.layout("4*1"):
            tgb.date("{date_init}", label="Departure Date", with_time=False)
            tgb.date("{date_end}", label="Return Date", with_time=False)
            tgb.selector(value="{departure}",label="Departure City", lov="{cities}", dropdown=True, on_change=on_change)
            tgb.selector(value="{arrival}",label="Arrival City", lov="{cities}", default="{arrival}",dropdown=True, on_change=on_change)

        tgb.text(value="#### \nSelect your preferences", mode="md", color="primary", align="center")

        with tgb.layout("4*1"):
            tgb.selector(value= "{selected_categories}", label = "Categories", lov = "{categories}", multiple = True, dropdown=True, on_change=on_change)
            tgb.selector(value= "{selected_activities}", label = "Activities", lov = "{activities}", multiple = True, dropdown=True, on_change=on_change)
        with tgb.part(render = "{init}"):
            tgb.text(value="####\n", mode="md")
    
        tgb.button("Meet People", color="primary", size="lg", block=True, on_action=change_init, active="{all_fields}")


with tgb.Page(on_refresh=default_values) as feed:
    with tgb.part(render="{start_again}"):
        tgb.text(value="# Feed", mode="md", color="primary", align="center")
        print("Events2: ", events)
        tgb.text("{events}")
                
        tgb.button("Start Again", color="secondary", size="lg", block=True, on_action=default_values, on_change=on_change)



    


pages = {
    "/" : root_page,
    "feed" : feed
}

if __name__ == "__main__":
    app = Gui(pages=pages)
    app.run(debug=True, use_reloader=True)