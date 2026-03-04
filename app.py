import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Production License Verification (POST Method)
def verify_license(key):
    try:
        # Pulls the LIVE API Key from your Streamlit Secrets
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        # This is the official validation endpoint
        url = "https://api.lemonsqueezy.com/v1/license-keys/validate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        
        # Packaging the user's license key in a JSON body
        payload = {"license_key": key}
        
        # We use POST here because it's required for newer Lemon Squeezy accounts
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("valid", False)
        
        # Logging errors for you to see in Streamlit 'Manage App' logs
        print(f"Lemon Squeezy API Error: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"Auth System Error: {e}")
        return False

# 3. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    
    authenticated = False
    if user_key:
        # Immediately check the key using the new POST logic
        if verify_license(user_key):
            st.success("PRO License Active")
            authenticated = True
        else:
            st.error("Invalid License Key")
    else:
        st.warning("License Required")

# 4. Main Application (Only runs if authenticated is True)
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://example.com")
    niche = st.text_input("Business Niche", placeholder="e.g., Mortgage Broker")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please enter both a URL and a Niche.")
        else:
            # Connect to Google Gemini
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # Professional Safety Settings (Block nothing for audits)
            safety = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
            
            with st.spinner("Processing Professional Audit..."):
                try:
                    prompt = f"Perform a professional GEO audit for {target_url} in the {niche} niche."
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
