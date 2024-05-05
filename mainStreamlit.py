import streamlit as st
from controller import getEvents

interests = ['Art Exhibitions', 'Beach Volleyball', 'Concerts', 'Cooking Classes', 'Cultural Festivals', 'Dancing Classes', 'Escape Rooms', 'Food Tours', 'Football Matches', 'Group Cycling Tours', 'Hiking Excursions', 'Hot Air Balloon Rides', 'Karaoke Nights', 'Kayaking', 'Pub Crawls', 'River Cruises', 'Rock Climbing', 'Scavenger Hunts', 'Segway Tours', 'Sightseeing Tours', 'Snorkeling Tours', 'Theater Performances', 'Theme Parks', 'Wine Tasting', 'Zip Line Adventures']
cities = ['Amsterdam', 'Barcelona', 'Berlin', 'Brussels', 'Budapest', 'Dublin', 'Florence', 'Lisbon', 'London', 'Madrid', 'Milan', 'Munich', 'Paris', 'Prague', 'Rome', 'Vienna', 'Zurich']

def main():
    st.text("Welcome Traveler")
    start_date = st.date_input(label='Departure day')
    return_date = st.date_input(label='Return day')
    departure_city = st.selectbox(label='Departure City', options=cities)
    arrival_city = st.selectbox(label='Arrival city', options=cities)
    activities = st.multiselect(label="Interests", options=interests)
    button = st.button("Meet new people")
    if button:
        results = getEvents(start_date, return_date, arrival_city, activities)
        print(results)
        for result in results:
            event, persones = result
            st.text(event.name)
            st.image(
                event.imageURL,
                width=400, # Manually Adjust the width of the image as per requirement
            )
            st.write("Date: " + event.date)
            st.write("Venue: ", event.venue)
            st.write("Link: ", event.pageLink)
            
            res = ""
            for ind, persona in enumerate(persones):
                if ind == 0:
                    res += persona
                else:
                    res += ", "
                    res += persona

            st.write("People interested: ", res)

if __name__ == "__main__":
    main()

        


