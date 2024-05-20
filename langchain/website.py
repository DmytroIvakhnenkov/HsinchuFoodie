import streamlit as st
import requests
import googlemaps
import dotenv
import os 
from chatbot import ChatBot

# Set up Google Places API
LOCATION = 'Hsinchu, Taiwan'
SEARCH_QUERY = 'burger'
dotenv.load_dotenv()
MAPS_KEY = os.getenv('MAPS_KEY')
gmaps = googlemaps.Client(key=MAPS_KEY)
import json

# Define bubble styles
bubble_style = """
<style>
.bubble {
    display: inline-block;
    padding: 10px 20px;
    margin: 5px;
    border: 2px solid;
    border-radius: 25px;
    background-color: transparent;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
}
.bubble.red { border-color: #FF6347; color: #FF6347; }
.bubble.green { border-color: #32CD32; color: #32CD32; }
.bubble.gray { border-color: #dcdcdc; color: #dcdcdc; }
</style>
"""

# Define a function to create a bubble
def create_bubble(text, color_class):
    return f'<span class="bubble {color_class}">{text}</span>'


def get_restaurants():
    geocode_result = gmaps.geocode(LOCATION)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    places = gmaps.places_nearby(
                keyword="burgers",
                radius = "1000",
                location=[lat,lng],
                language="en",
            )
    return places

def diplay_summary(place_details):
    if place_details["reviews"]:
        question = ""
        for i, review in enumerate(place_details["reviews"]):
            question += f"Review {i}: {review}\n"
        chat = ChatBot()
        answer = chat.call_chat(question).content
        json_start = answer.find('{')
        json_end = answer.rfind('}') + 1
        json_str = answer[json_start:json_end]
        parsed_data = json.loads(json_str)
        st.write(parsed_data["summary"])
        words_with_colors = []
        for neutral in parsed_data["positive_features"]:
            words_with_colors.append((neutral, "green"))
        for neutral in parsed_data["neutral_features"]:
            words_with_colors.append((neutral, "gray"))
        for neutral in parsed_data["negative_features"]:
            words_with_colors.append((neutral, "red"))
        # List of words and their corresponding colors
        bubbles_html = "".join([create_bubble(word, color) for word, color in words_with_colors])
        st.markdown(bubbles_html, unsafe_allow_html=True)

def main():


    # Display the bubbles
    st.markdown(bubble_style, unsafe_allow_html=True)

    st.title("Top Burger Restaurants in Hsinchu")
    
    st.write("Fetching top-rated burger restaurants in Hsinchu, Taiwan...") 
    # Fetch data

    data = get_restaurants()
    if data:
        results = data.get('results', [])
        if results:
            results = sorted(results, key=lambda x: x.get('rating', 0), reverse=True)
            for p, place in enumerate(results):
                name = place.get('name')
                rating = place.get('rating', 'N/A')
                place_id = place.get('place_id')
                place_details = gmaps.place(place_id)["result"]
                address = place.get('formatted_address')
                st.subheader(name)
                st.write(f"Rating: {rating}")
                # st.write(f"Address: {address}")
                if st.button('Get reviews summary', key=p):
                    diplay_summary(place_details)
                # Create a button
                
                st.write("---")
        else:
            st.write("No results found.")
    else:
        st.write("Failed to retrieve data.")

if __name__ == "__main__":
    main()
