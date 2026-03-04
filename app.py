import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration (Strictly Professional)
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. License Verification Logic (The Original Working Method)
def verify_license(key):
    try:
        # Accesses the secret name currently in your settings
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
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
        print(f"Auth System Error: {e}")
        return False

# 3. Sidebar Authentication
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
    niche = st.text_input("Business Niche", placeholder="e.g., Mortgage Broker")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please enter both a URL and a Niche.")
        else:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # Safety bypass to ensure audits aren't blocked for professional niches
            safety = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
            
            with st.spinner("Processing..."):
                try:
                    prompt = f"Perform a professional GEO audit for {target_url} in the {niche} niche."
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
