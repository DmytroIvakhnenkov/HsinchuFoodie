import streamlit as st
import requests
import googlemaps
import dotenv
import os

# Set up Google Places API
LOCATION = 'Hsinchu, Taiwan'
SEARCH_QUERY = 'burger'
dotenv.load_dotenv()
MAPS_KEY = os.getenv('MAPS_KEY')
gmaps = googlemaps.Client(key=MAPS_KEY)


def get_restaurants():
    geocode_result = gmaps.geocode(LOCATION)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    places = gmaps.places_nearby(
                keyword="burgers",
                radius = "3000",
                location=[lat,lng],
                language="en",
            )
    return places

def main():
    st.title("Top Burger Restaurants in Hsinchu")
    
    st.write("Fetching top-rated burger restaurants in Hsinchu, Taiwan...") 
    # Fetch data
    
    data = get_restaurants()
    if data:
        results = data.get('results', [])
        if results:
            results = sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
            for place in results:
                name = place.get('name')
                rating = place.get('rating', 'N/A')
                # address = place.get('formatted_address')
                st.subheader(name)
                st.write(f"Rating: {rating}")
                # st.write(f"Address: {address}")
                st.write("---")
        else:
            st.write("No results found.")
    else:
        st.write("Failed to retrieve data.")

if __name__ == "__main__":
    main()
