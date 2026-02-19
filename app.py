import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- 1. CONFIGURATION (Replace these with your actual IDs) ---
# You get these from your Lemon Squeezy Dashboard
LEMON_SQUEEZY_API_URL = "https://api.lemonsqueezy.com/v1/licenses/validate"

# --- 2. LICENSE CHECK FUNCTION ---
def is_license_valid(key):
    try:
        # We send a request to Lemon Squeezy to check the key
        response = requests.post(
            LEMON_SQUEEZY_API_URL,
            data={"license_key": key},
            headers={"Accept": "application/json"}
        )
        data = response.json()
        return data.get("valid", False)
    except:
        return False

# --- 3. THE LOCK SCREEN ---
st.set_page_config(page_title="Limon Media GEO Auditor", page_icon="🚀")

# Check if the user is already "Logged In" for this session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Pro Tool Locked")
    st.write("Please enter your license key from the **Limon Media Store** to continue.")
    
    user_key = st.text_input("License Key", type="password")
    if st.button("Unlock Tool"):
        if is_license_valid(user_key):
            st.session_state["authenticated"] = True
            st.success("License Activated!")
            st.rerun()
        else:
            st.error("Invalid License Key. Please check your email or store account.")
    
    st.info("Don't have a key? [Get one here at the Limon Media Store](https://yourstorelink.com)")
    st.stop() # This stops the rest of the code from running

# --- 4. THE ACTUAL TOOL (Only runs if authenticated) ---
st.title("🌐 AI Overview (GEO) Auditor")
# ... (The rest of your existing audit code goes here) ...
st.sidebar.button("Log Out", on_click=lambda: st.session_state.update({"authenticated": False}))
