import streamlit as st
import pandas as pd
import requests
import os


st.set_page_config(page_title="Swiggy Registration", layout="centered")

# Page Title
st.title("🍽️ Swiggy Partner Registration")

# Registration Form
with st.form("registration_form"):
    st.header("Register as a Delivery Partner")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    city = st.text_input("City")
    vehicle = st.selectbox("Vehicle Type", ["Bicycle", "Bike", "Scooter", "Car"])
    experience = st.radio("Do you have delivery experience?", ["Yes", "No"])
    agree = st.checkbox("I agree to the Terms and Conditions")

    submit = st.form_submit_button("Register")

    if submit:
        if not agree:
            st.error("You must agree to the Terms and Conditions to proceed.")
        elif not full_name or not email or not phone or not city:
            st.warning("Please fill in all required fields.")
        else:
            st.success(f"🎉 Thanks for registering, {full_name}!")
            st.info("Our team will contact you soon via email or phone.")

# Optional Footer
st.markdown("---")
st.markdown("🚀 Built with ❤️ using Streamlit")



# Swiggy pseudo API integration
def swiggy_search(query, pin_code, allergy):
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
