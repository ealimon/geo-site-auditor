import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. THE FIX: Official Lemon Squeezy License API Logic
def verify_license(license_key):
    try:
        # Get and clean the API key from Secrets
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"].strip().strip('"').strip("'")
        
        # URL for the LICENSE API (not the general store API)
        url = "https://api.lemonsqueezy.com/v1/license-keys/validate"
        
        # REQUIRED HEADERS for the License API
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # THE CRITICAL CHANGE: License API expects form data, not JSON
        payload = {"license_key": license_key}
        
        # Send as data=payload (form-encoded) instead of json=payload
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Returns True if 'valid' is true in the response body
            return data.get("valid", False)
        
        # Logs the specific error code (e.g., 401, 422) to Streamlit Logs
        print(f"License API Error: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"System Auth Error: {e}")
        return False

# 3. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password")
    
    authenticated = False
    if user_key:
        with st.spinner("Checking Live Database..."):
            if verify_license(user_key):
                st.success("PRO License Active")
                authenticated = True
            else:
                st.error("Invalid License Key")
                st.info("Ensure you are using a LIVE key (not a test key).")
    else:
        st.warning("License Required")

# 4. Main Application
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://example.com")
    niche = st.text_input("Business Niche", placeholder="e.g., Dentist in London")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please fill in both fields.")
        else:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Analyzing..."):
                try:
                    prompt = f"Perform a professional GEO audit for {target_url} in the {niche} niche."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

st.divider()
st.caption("Powered by Limon Media © 2026")
