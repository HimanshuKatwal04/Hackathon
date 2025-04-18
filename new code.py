import streamlit as st
import pandas as pd
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
            'Spice Tolerance', 'Delivery Preference', 'Preferred Meal Time'
        ])

def save_user(user_data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Dummy AI recommendation agent
def recommend_food(query, user_data):
    allergy = user_data['Allergy']
    pin_code = user_data['Pin Code']
    food_type = user_data['Food Preference']
    cuisine = user_data['Preferred Cuisine']
    
    # This is where you can call an actual AI agent or API
    results = [
        {
            'Restaurant': 'Healthy Bites',
            'Item': f'Gluten-Free {query.title()}',
            'Cuisine': cuisine,
            'Price': '₹250',
            'Location': f'Near {pin_code}'
        },
        {
            'Restaurant': 'Organic Eats',
            'Item': f'{query.title()} (No {allergy})',
            'Cuisine': cuisine,
            'Price': '₹280',
            'Location': f'Within 3 km of {pin_code}'
        },
    ]
    return results

# App Interface
st.title("🍽️ Smart Food Finder")
menu = st.sidebar.selectbox("Choose an option", ["Register", "Search"])

if menu == "Register":
    st.subheader("New User Registration")

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
    meal_time = st.selectbox("Preferred Meal Time", ['Breakfast', 'Lunch', 'Dinner', 'Snacks'])

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
            'Delivery Preference': delivery,
            'Preferred Meal Time': meal_time
        }
        save_user(user)
        st.success("User Registered Successfully!")

elif menu == "Search":
    st.subheader("Search Food / Restaurants / Brands")

    name = st.text_input("Enter your registered name to fetch preferences")

    df = load_data()
    if name and name in df['Name'].values:
        user_data = df[df['Name'] == name].iloc[0].to_dict()
        query = st.text_input("Search for a dish, drink, or restaurant")

        if st.button("Search"):
            st.info(f"Showing results near {user_data['Pin Code']} with allergy filter: {user_data['Allergy']}")
            results = recommend_food(query, user_data)

            for r in results:
                st.markdown(f"""
                    **🍴 {r['Item']}**  
                    🏨 *{r['Restaurant']}*  
                    🌶️ Cuisine: {r['Cuisine']}  
                    💸 Price: {r['Price']}  
                    📍 Location: {r['Location']}  
                    ---
                """)
    else:
        if name:
            st.error("User not found. Please register first.")
