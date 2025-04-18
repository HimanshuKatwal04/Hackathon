import streamlit as st
import os
import json
from datetime import datetime

# Define the path to save the registered user data
file_path = "/mnt/data/swiggy_streamlit_app.py"

# Initialize session state
if "registered_users" not in st.session_state:
    st.session_state.registered_users = []

# Load existing users if the file exists
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        try:
            st.session_state.registered_users = json.load(f)
        except json.JSONDecodeError:
            st.session_state.registered_users = []

# Registration form
st.title("🍽️ Swiggy-style Food App")
st.subheader("Register")

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    fav_cuisine = st.selectbox("Favorite Cuisine", ["Indian", "Italian", "Chinese", "Mexican", "Thai", "American"])
    register = st.form_submit_button("Register")

    if register:
        if username and email:
            user_data = {
                "username": username,
                "email": email,
                "fav_cuisine": fav_cuisine,
                "registered_on": str(datetime.now())
            }
            st.session_state.registered_users.append(user_data)

            # Save updated user data
            with open(file_path, "w") as f:
                json.dump(st.session_state.registered_users, f)

            st.success(f"🎉 Welcome, {username}! You've been registered successfully.")
        else:
            st.error("Please enter both username and email.")

# View Registered Users
st.subheader("📋 Registered Users")
if st.session_state.registered_users:
    for user in st.session_state.registered_users:
        st.markdown(f"""
        **Username:** {user['username']}  
        **Email:** {user['email']}  
        **Favorite Cuisine:** {user['fav_cuisine']}  
        **Registered On:** {user['registered_on']}  
        ---
        """)
else:
    st.info("No users registered yet.")
