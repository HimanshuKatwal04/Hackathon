# Prepare the basic structure for the Streamlit app with Swiggy integration placeholder
streamlit_app_code = '''
import streamlit as st
import pandas as pd
import requests
import os

DATA_FILE = "Hackathon Dataset - Sheet1.csv"

# Load or initialize dataset
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            'Name', 'Age', 'Sex', 'State', 'City', 'Pin Code',
            'Allergy', 'Food Preference', 'Preferred Cuisine',
            'Spice Tolerance', 'Delivery Preference'
        ])

def save_user(user_data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Swiggy pseudo API integration (replace with actual proxy if needed)
def swiggy_search(query, pin_code, allergy):
    # Placeholder logic simulating a Swiggy API response
    # Replace this with actual proxy API logic or scraped data endpoint
    dummy_results = [
        {
            'Restaurant': 'Pizza Palace',
            'Item': 'Gluten-Free Veg Pizza',
            'Price': '₹299',
            'Rating': '4.5',
            'Distance': '2.1 km',
            'Allergy Safe': 'Yes' if allergy.lower() not in 'gluten' else 'No'
        },
        {
            'Restaurant': 'Crusty Cravings',
            'Item': 'Cheese Burst Jain Pizza',
            'Price': '₹320',
            'Rating': '4.2',
            'Distance': '3.0 km',
            'Allergy Safe': 'Yes'
        }
    ]
    # Filter by allergy
    return [r for r in dummy_results if r['Allergy Safe'] == 'Yes']

# Streamlit Interface
st.title("🍲 Swiggy Smart Food Finder")
menu = st.sidebar.selectbox("Choose an option", ["Register", "Search"])

if menu == "Register":
    st.subheader("User Registration")

    name = st.text_input("Name")
    age = st.number_input("Age", 18, 100)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    state = st.text_input("State")
    city = st.text_input("City")
    pin_code = st.text_input("Pin Code")

    allergy = st.selectbox("Allergy", ['None', 'Gluten', 'Lactose', 'Peanuts', 'Soy', 'Shellfish', 'Eggs'])
    food_pref = st.selectbox("Food Preference", ['Veg', 'Non-Veg', 'Jain'])
    cuisine = st.selectbox("Preferred Cuisine", ['Indian', 'Chinese', 'Italian', 'Mexican', 'Thai', 'Continental'])
    spice = st.selectbox("Spice Tolerance", ['Low', 'Medium', 'High'])
    delivery = st.selectbox("Delivery Preference", ['Home Delivery', 'Pickup', 'Dine-In'])

    if st.button("Submit"):
        user = {
            'Name': name,
            'Age': age,
            'Sex': sex,
            'State': state,
            'City': city,
            'Pin Code': pin_code,
            'Allergy': allergy,
            'Food Preference': food_pref,
            'Preferred Cuisine': cuisine,
            'Spice Tolerance': spice,
            'Delivery Preference': delivery
        }
        save_user(user)
        st.success("User Registered Successfully!")

elif menu == "Search":
    st.subheader("Search Restaurants or Food")

    name = st.text_input("Enter your registered name")

    df = load_data()
    if name and name in df['Name'].values:
        user_data = df[df['Name'] == name].iloc[0].to_dict()
        query = st.text_input("Search for food or restaurant")

        if st.button("Search"):
            st.info(f"Fetching results for {query} near {user_data['Pin Code']} considering allergy: {user_data['Allergy']}")
            results = swiggy_search(query, user_data['Pin Code'], user_data['Allergy'])

            for r in results:
                st.markdown(f"""
                **🍽️ {r['Item']}**  
                🏬 *{r['Restaurant']}*  
                💸 Price: {r['Price']}  
                ⭐ Rating: {r['Rating']}  
                📍 Distance: {r['Distance']}  
                ✅ Allergy Safe: {r['Allergy Safe']}  
                ---
                """)
    else:
        if name:
            st.error("User not found. Please register first.")
'''

# Save the new Streamlit app code to a file
file_path = "/mnt/data/swiggy_streamlit_app.py"
with open(file_path, "w") as f:
    f.write(streamlit_app_code)

file_path
