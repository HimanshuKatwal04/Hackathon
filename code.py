# Prototype: AI Agent-Based Food & Beverage Recommendation System (Streamlit UI)

import streamlit as st
import pandas as pd

# Load Customer Dataset
df = pd.read_csv("/content/indian_fnb_customers.csv")

# -------------------------
# Agent Functions
# -------------------------

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
    return [
        p for p in products if
        (p['price'] <= profile['budget']) and
        (profile['allergy'] not in p['tags']) and
        (profile['food_pref'].lower() in p['tags'])
    ]

def location_agent(products, city, pincode):
    return [
        p for p in products if (p['city'] == city and pincode in p['pincodes'])
    ]

def search_products(search_term):
    # Simulate real-time scraped/API data from Zomato, Swiggy, Instamart
    sample_data = [
        {"name": "Paneer Tikka - Zomato", "price": 250, "url": "https://zomato.com/paneer-tikka", "tags": ["vegetarian"], "city": "Mumbai", "pincodes": [400001, 400002]},
        {"name": "Grilled Chicken - Swiggy", "price": 300, "url": "https://swiggy.com/grilled-chicken", "tags": ["non-vegetarian"], "city": "Mumbai", "pincodes": [400001]},
        {"name": "Vegan Salad - Instamart", "price": 200, "url": "https://swiggy.com/vegan-salad", "tags": ["vegan"], "city": "Mumbai", "pincodes": [400002]},
        {"name": "Jain Thali - Zomato", "price": 350, "url": "https://zomato.com/jain-thali", "tags": ["jain"], "city": "Mumbai", "pincodes": [400001]},
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
        profile = customer_profile_agent(name_input)

        st.subheader("Customer Profile")
        st.json(profile)

        results = search_products(search_term)
        loc_filtered = location_agent(results, profile['city'], profile['pincode'])
        final_recommendations = filter_agent(loc_filtered, profile)

        st.subheader("Recommended for You")
        if final_recommendations:
            for item in final_recommendations:
                st.markdown(f"**{item['name']}** - ₹{item['price']}  ")
                st.markdown(f"[View on Platform]({item['url']})")
                st.markdown("---")
        else:
            st.warning("No matching products found in your area with your preferences.")

if __name__ == "__main__":
    main()
