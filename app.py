import streamlit as st
import google.generativeai as genai
import requests

# 1. Setup Page Config & Branding
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Authentication Logic (Lemon Squeezy)
def verify_license(key):
    try:
        # Pulls from your Streamlit Secrets
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/vnd.api+json"}
        # Validates the key against Lemon Squeezy's database
        response = requests.get(f"https://api.lemonsqueezy.com/v1/license-keys/validate?license_key={key}", headers=headers)
        return response.json().get("valid", False)
    except:
        return False

# Sidebar for License Entry
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    
    if user_key:
        if verify_license(user_key):
            st.success("PRO License Active") #
            st.info("🚀 150-Audit Agency License Loaded") #
            authenticated = True
        else:
            st.error("Invalid License Key")
            authenticated = False
    else:
        st.warning("License Required: Please enter your key to begin.")
        st.button("Get Your Agency License")
        authenticated = False

# 3. Main Audit Logic (Unlocked if Authenticated)
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://www.example.com") #
    niche = st.text_input("Business Niche", placeholder="e.g., mortgage broker") #

    if st.button("Generate Professional AI Audit"):
        # Configure Gemini with safety bypass
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Safety Settings: Set to BLOCK_NONE to prevent 'Invalid operation' errors in professional niches
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

        with st.spinner("Searching for available AI Brain..."): #
            try:
                # Custom System Prompt for GEO Strategy
                prompt = f"Perform a professional GEO Audit for {target_url} in the {niche} niche. Identify content gaps for AI search and provide JSON-LD schema recommendations."
                response = model.generate_content(prompt)
                
                # Check if the response was blocked despite settings
                if response.candidates[0].finish_reason != 1:
                     st.markdown(response.text)
                else:
                     st.error("Technical Alert: The AI declined to answer this specific query due to its internal safety layers. Try rephrasing the niche.")
                     
            except Exception as e:
                st.error(f"Technical Alert: {str(e)}") # Catches the 'Part' error

# 4. Footer Branding
st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
