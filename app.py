import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration (Strictly Professional)
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. License Verification Logic
def verify_license(key):
    try:
        # Access the secret key from your Streamlit settings
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        # Original working GET request structure
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
        # This will show in your Streamlit logs if there's a connection error
        print(f"System Error: {e}")
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

# 4. Main Application Logic
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://vanmarlending.com")
    niche = st.text_input("Business Niche", placeholder="e.g., Mortgage Broker")

    if st.button("Generate Professional AI Audit"):
        if not target_url or not niche:
            st.warning("Please provide both a URL and a Niche.")
        else:
            # Initialize Gemini
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # Safety settings to prevent audits from being blocked in professional niches
            safety = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
            
            with st.spinner("Analyzing Site for GEO Gaps..."):
                try:
                    prompt = (
                        f"Act as a GEO expert. Audit {target_url} for the '{niche}' niche. "
                        f"1. Identify missing 'Atomic Answers' for AI search. "
                        f"2. Suggest specific JSON-LD schema improvements. "
                        f"3. Rank the site's AI-readiness from 1-10."
                    )
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI Technical Alert: {e}")

# 5. Footer
st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
