import streamlit as st
import json
import os

# File to store user data
USER_DATA_FILE = "users.json"

# Load existing users
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user
def save_user(user):
    users = load_users()
    users[user["name"]] = user
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Registration page
def registration_page():
    st.title("New User Registration")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    state = st.text_input("State")
    city = st.text_input("City")
    pin_code = st.text_input("Pin Code")
    allergies = st.text_input("Allergies (comma-separated)")

    if st.button("Register"):
        user = {
            "name": name,
            "age": age,
            "gender": gender,
            "state": state,
            "city": city,
            "pin_code": pin_code,
            "allergies": [a.strip().lower() for a in allergies.split(",")],
        }
        save_user(user)
        st.session_state.user = user
        st.success("Registered successfully!")
        st.experimental_rerun()

# Search & Recommendation Page
def recommendation_page(user):
    st.title("Search Restaurants and Food")
    query = st.text_input("Search for food, drinks, or brands")

    if query:
        with st.spinner("Fetching recommendations..."):
            results = get_recommendations(query, user)
            st.subheader(f"Results for '{query}':")
            for item in results:
                st.markdown(f"""
                **{item['name']}**  
                📍 {item['location']}  
                💰 {item['price']}  
                ⭐ {item['rating']}  
                🔗 [View]({item['url']})
                ---
                """)

# Dummy Recommendation Engine (Replace with real scraping/api)
def get_recommendations(query, user):
    allergy_filter = user["allergies"]
    pin = user["pin_code"]

    # Placeholder response
    mock_results = [
        {"name": "Pizza Palace (Gluten Free)", "location": "Nearby", "price": "₹299", "rating": 4.5, "url": "#"},
        {"name": "Healthy Slice", "location": "1.2km away", "price": "₹349", "rating": 4.2, "url": "#"},
    ]

    # Filter based on allergy (if not gluten-free, exclude)
    filtered = [r for r in mock_results if "gluten" in " ".join(allergy_filter).lower() and "gluten free" in r["name"].lower()]
    return filtered or mock_results

# App Entry Point
def main():
    st.set_page_config(page_title="Smart Food Recommender", layout="wide")

    if "user" not in st.session_state:
        registration_page()
    else:
        recommendation_page(st.session_state.user)

if __name__ == "__main__":
    main()
