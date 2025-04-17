import streamlit as st
import pandas as pd
import random

# -------------------------
# Generate Customer Dataset
# -------------------------

names = ['Rohan Mehta', 'Priya Sharma', 'Aarav Verma', 'Sneha Nair', 'Rahul Das', 'Ananya Iyer', 'Karan Singh', 'Isha Patel']
states = ['Maharashtra', 'Karnataka', 'West Bengal', 'Delhi', 'Tamil Nadu', 'Gujarat']
cities = {
    'Maharashtra': ['Mumbai', 'Pune'],
    'Karnataka': ['Bengaluru', 'Mysuru'],
    'West Bengal': ['Kolkata', 'Siliguri'],
    'Delhi': ['New Delhi', 'Dwarka'],
    'Tamil Nadu': ['Chennai', 'Coimbatore'],
    'Gujarat': ['Ahmedabad', 'Surat']
}
pincodes = {
    'Mumbai': [400001, 400002], 'Pune': [411001, 411002],
    'Bengaluru': [560001, 560002], 'Mysuru': [570001, 570002],
    'Kolkata': [700001, 700002], 'Siliguri': [734001, 734002],
    'New Delhi': [110001, 110002], 'Dwarka': [110075, 110078],
    'Chennai': [600001, 600002], 'Coimbatore': [641001, 641002],
    'Ahmedabad': [380001, 380002], 'Surat': [395001, 395002]
}
genders = ['Male', 'Female', 'Other']
allergies = ['None', 'Peanuts', 'Gluten', 'Lactose', 'Seafood']
food_prefs = ['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Jain']
browsing_devices = ['Mobile', 'Desktop', 'Tablet']

data = []
for i in range(100):
    name = random.choice(names)
    age = random.randint(18, 60)
    sex = random.choice(genders)
    state = random.choice(states)
    city = random.choice(cities[state])
    pincode = random.choice(pincodes[city])
    allergy = random.choice(allergies)
    food_pref = random.choice(food_prefs)
    device = random.choice(browsing_devices)
    budget = random.choice([200, 300, 500, 1000, 1500])  # INR

    data.append([name, age, sex, state, city, pincode, allergy, food_pref, device, budget])

df = pd.DataFrame(data, columns=[
    'Name', 'Age', 'Sex', 'State', 'City', 'Pincode',
    'Allergy', 'Food Preference', 'Device', 'Budget (INR)'
])

# -------------------------
# Agent Functions
# -------------------------

def normalize_tag(tag):
    return tag.strip().lower().replace("-", "").replace("_", "")

def customer_profile_agent(name):
    customer = df[df['Name'] == name].iloc[0]
    return {
        "age": customer['Age'],
        "sex": customer['Sex'],
        "city": customer['City'],
        "pincode": customer['Pincode'],
        "allergy": customer['Allergy'],
        "food_pref": customer['Food Preference'],
        "budget": customer['Budget (INR)']
    }

def filter_agent(products, profile):
    pref = normalize_tag(profile['food_pref'])
    allergy = normalize_tag(profile['allergy'])
    return [
        p for p in products if
        (p['price'] <= profile['budget']) and
        (allergy != "none" and allergy not in map(normalize_tag, p['tags']) or allergy == "none") and
        (pref in map(normalize_tag, p['tags']))
    ]

def location_agent(products, city, pincode):
    return [
        p for p in products if (p['city'] == city and pincode in p['pincodes'])
    ]

def search_products(search_term):
    sample_data = [
        {
            "name": "Paneer Tikka - Zomato", "price": 250,
            "url": "https://zomato.com/paneer-tikka",
            "tags": ["vegetarian"], "city": "Mumbai", "pincodes": [400001, 400002],
            "image": "https://via.placeholder.com/150?text=Paneer+Tikka"
        },
        {
            "name": "Grilled Chicken - Swiggy", "price": 300,
            "url": "https://swiggy.com/grilled-chicken",
            "tags": ["non-vegetarian"], "city": "Mumbai", "pincodes": [400001],
            "image": "https://via.placeholder.com/150?text=Grilled+Chicken"
        },
        {
            "name": "Vegan Salad - Instamart", "price": 200,
            "url": "https://swiggy.com/vegan-salad",
            "tags": ["vegan"], "city": "Mumbai", "pincodes": [400002],
            "image": "https://via.placeholder.com/150?text=Vegan+Salad"
        },
        {
            "name": "Jain Thali - Zomato", "price": 350,
            "url": "https://zomato.com/jain-thali",
            "tags": ["jain"], "city": "Mumbai", "pincodes": [400001],
            "image": "https://via.placeholder.com/150?text=Jain+Thali"
        },
    ]
    return [item for item in sample_data if search_term.lower() in item['name'].lower()]

# -------------------------
# Streamlit UI
# -------------------------

def main():
    st.title("🍽️ AI Food & Beverage Recommender")

    names = df['Name'].unique().tolist()
    name_input = st.selectbox("Select a customer", names)
    search_term = st.text_input("Search for a product/brand/restaurant")

    if st.button("Find Recommendations") and search_term:
        with st.spinner("Finding the best options for you..."):
            profile = customer_profile_agent(name_input)

            st.subheader("👤 Customer Profile")
            st.json(profile)

            results = search_products(search_term)
            loc_filtered = location_agent(results, profile['city'], profile['pincode'])
            final_recommendations = filter_agent(loc_filtered, profile)

            st.subheader("✨ Recommended for You")
            if final_recommendations:
                for item in final_recommendations:
                    st.image(item['image'], width=150)
                    st.markdown(f"**{item['name']}** - ₹{item['price']}")
                    st.markdown(f"[View on Platform]({item['url']})")
                    st.markdown("---")
            else:
                st.warning("No matching products found in your area with your preferences.")

if __name__ == "__main__":
    main()
