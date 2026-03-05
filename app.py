import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. License Verification (Lemon Squeezy)
def verify_license(license_key):
    try:
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"].strip().strip('"').strip("'")
        url = "https://api.lemonsqueezy.com/v1/licenses/validate"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
        payload = {"license_key": license_key}
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get("valid", False) if response.status_code == 200 else False
    except:
        return False

# 3. Smart Model Selector
def get_best_model():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for preferred in ['gemini-3-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']:
            for m in models:
                if preferred in m: return m
        return models[0]
    except:
        return "gemini-1.5-flash"

# 4. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    st.info("Check your email for your license key.")
    
    authenticated = False
    if user_key:
        if verify_license(user_key):
            st.success("PRO License Active")
            authenticated = True
        else:
            st.error("Invalid License Key")
    else:
        st.warning("License Required")

# 5. Main Application Logic
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://example.com")
    niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please fill in both fields.")
        else:
            try:
                # Use the smart selector to avoid 404s
                model_name = get_best_model()
                model = genai.GenerativeModel(model_name)
                
                with st.spinner(f"Analyzing via {model_name}..."):
                    prompt = f"Perform a professional GEO audit for {target_url} in the {niche} niche. Focus on AI search visibility."
                    response = model.generate_content(prompt)
                    
                    # Display the successful results on screen
                    st.divider()
                    st.markdown(response.text)
            
            except Exception as e:
                # Handle the 429 quota error seen in your earlier tests
                if "429" in str(e):
                    st.error("Speed Limit Reached. Please wait 60 seconds and try again.")
                else:
                    st.error(f"Audit Error: {str(e)}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
