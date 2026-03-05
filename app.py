import streamlit as st
import google.generativeai as genai
import requests
import time

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Verified License Logic (Lemon Squeezy Handshake)
def verify_license(license_key):
    try:
        # Clean the API key from Streamlit Secrets
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"].strip().strip('"').strip("'")
        
        # Dedicated license validation endpoint
        url = "https://api.lemonsqueezy.com/v1/licenses/validate"
        headers = {
            "Accept": "application/json", 
            "Authorization": f"Bearer {api_key}"
        }
        
        # Payload must be form-data (data=)
        payload = {"license_key": license_key}
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            return response.json().get("valid", False)
        return False
    except:
        return False

# 3. Smart Model Selector (Detects available Gemini versions)
def get_best_model():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Fetches only models that support content generation
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority check for the most modern 2026 models
        for preferred in ['gemini-3-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']:
            for m in models:
                if preferred in m: 
                    return m
        return models[0] # Fallback to first available
    except:
        return "gemini-1.5-flash"

# 4. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    
    # Instruction as requested
    st.info("Check your email for your license key.")
    
    authenticated = False
    if user_key:
        # Verification happens here; badge turns green on success
        if verify_license(user_key):
            st.success("PRO License Active")
            authenticated = True
        else:
            st.error("Invalid License Key")
    else:
        st.warning("License Required")

# 5. Main Application (Unlocked after License check)
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://limon.media")
    niche = st.text_input("Business Niche", placeholder="e.g., Digital Marketing Agency")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please provide both a URL and a Niche.")
        else:
            try:
                # Find the best model to avoid 404 errors
                model_name = get_best_model()
                model = genai.GenerativeModel(model_name)
