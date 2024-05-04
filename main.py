from taipy import Gui
from datetime import datetime
import taipy.gui.builder as tgb
import taipy as tp

cities = ['Amsterdam', 'Barcelona', 'Berlin', 'Brussels', 'Budapest', 'Dublin', 'Florence', 'Lisbon', 'London', 'Madrid', 'Milan', 'Munich', 'Paris', 'Prague', 'Rome', 'Vienna', 'Zurich']
dates = [datetime(2024, 1, 1), datetime(2024, 12, 31)]

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


init = True
start_again = False
def change_init(state):
    state.init = False
    state.start_again = True

def default_values(state):
    state.init = True
    state.start_again = False
    state.departure = ""
    state.arrival = ""

def on_change(state, var_name: str, value: any):
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



with tgb.Page(on_refresh=change_init) as root_page:
    tgb.text(value="# Welcome Traveler", mode="md", color="primary", align="center")
    with tgb.layout("5 2*1"):
        with tgb.part(render = "{init}"):
            tgb.date_range("{dates}", with_time=False)
        with tgb.part(render = "{init}"): 
            tgb.selector(value="{departure}",label="Departure", lov="{cities}", dropdown=True, on_change=on_change)
        with tgb.part(render = "{init}"):
            tgb.selector(value="{arrival}",label="Arrival", lov="{cities}", default="{arrival}",dropdown=True, on_change=on_change)

    with tgb.layout("5 2*1"):
        with tgb.part(render = "{init}"):
            pass
        with tgb.part(render = "{init}"):
            tgb.selector(value= "{selected_categories}", label = "Categories", lov = "{categories}", multiple = True, dropdown=True, on_change=on_change)
        with tgb.part(render = "{init}"):
            tgb.selector(value= "{selected_activities}", label = "Activities", lov = "{activities}", multiple = True, dropdown=True, on_change=on_change)
    
    with tgb.part(render = "{init}"):
        tgb.button("Meet People", color="primary", size="lg", block=True, on_action=change_init)
    with tgb.part(render = "{start_again}"):
        tgb.button("Start Again", color="secondary", size="lg", block=True, on_action=default_values, on_change=on_change)


pages = {
    "/" : root_page
}

if __name__ == '__main__':
    Gui(pages=pages).run(debug=True, use_reloader=True, )