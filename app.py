import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")

# Custom CSS for a professional UI
st.markdown("""
    <style>
    .main { opacity: 0.95; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("GEO Auditor PRO")

# 2. Production-Grade License Verification
def verify_license(key):
    """
    Validates license key using a POST request.
    Includes sanitization for long App Tokens (JWTs).
    """
    try:
        # 1. Pull the secret
        raw_api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        # 2. SANITIZE: Remove any accidental quotes or spaces from the Secret string
        api_key = raw_api_key.strip().replace('"', '').replace("'", "")
        
        url = "https://api.lemonsqueezy.com/v1/license-keys/validate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        
        payload = {"license_key": key}
        
        # 3. Use POST (required for modern JWT App Tokens)
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("valid", False)
        else:
            # This logs the specific error to your Streamlit 'Manage App' console
            print(f"LS API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Auth System Error: {e}")
        return False

# 3. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    st.info("Enter your PRO license key received via email.")
    
    user_key = st.text_input("Enter License Key", type="password", help="Format: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
    
    authenticated = False
    
    if user_key:
        with st.spinner("Validating with Lemon Squeezy..."):
            if verify_license(user_key):
                st.success("PRO License Active")
                authenticated = True
            else:
                st.error("Invalid License Key")
                st.caption("Check if your store is in LIVE mode (Toggle OFF).")
    else:
        st.warning("License Required")

# 4. Main Application Logic
if authenticated:
    st.subheader("Generate Professional GEO Audit")
    
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("Website URL", placeholder="https://example.com")
    with col2:
        niche = st.text_input("Business Niche", placeholder="e.g., HVAC in Miami")

    if st.button("Run AI Analysis"):
        if not target_url or not niche:
            st.warning("Both fields are required.")
        else:
            try:
                # Initialize Gemini
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                
                # Safety settings for professional business audits
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
                
                with st.spinner("Analyzing AI Search Visibility..."):
                    prompt = f"""
                    Perform a professional GEO (Generative Engine Optimization) audit for {target_url}.
                    Focus on the {niche} niche. 
                    Provide actionable insights on how to improve visibility in Gemini and Perplexity.
                    """
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"AI Audit Failed: {e}")

else:
    st.write("---")
    st.info("Please authenticate using the sidebar to access the GEO Auditor PRO features.")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
