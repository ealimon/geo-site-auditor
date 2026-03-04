import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Reverted Validation Logic (GET Method)
def verify_license(key):
    try:
        # Uses the secret name from your current settings
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        # Original GET URL structure
        url = f"https://api.lemonsqueezy.com/v1/license-keys/validate?license_key={key}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("valid", False)
        return False
    except Exception as e:
        # Logs to 'Manage app' console if a connection issue occurs
        print(f"Auth System Error: {e}")
        return False

# 3. Sidebar Authentication Gate
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    
    authenticated = False
    if user_key:
        if verify_license(user_key):
            st.success("PRO License Active")
            authenticated = True
        else:
            st.error("Invalid License Key")
    else:
        st.warning("License Required")

# 4. Main Application
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://example.com")
    niche = st.text_input("Business Niche", placeholder="e.g., HVAC Services")

    if st.button("Generate AI Audit"):
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Safety settings to prevent 'Invalid Part' errors in professional niches
        safety = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
        
        with st.spinner("Processing Audit..."):
            try:
                prompt = f"Perform a GEO audit for {target_url} in the {niche} niche. List 3 ways to improve AI search visibility."
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Technical Alert: {e}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
