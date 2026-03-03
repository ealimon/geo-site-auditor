import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO 🍋")

# 2. Robust License Verification Function
def verify_license(key):
    """
    Validates the license key via Lemon Squeezy POST request.
    """
    try:
        # Pull the secret you renamed to LEMON_SQUEEZY_API_KEY
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        url = "https://api.lemonsqueezy.com/v1/license-keys/validate"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        # Lemon Squeezy prefers POST for validation to keep keys out of URL logs
        data = {"license_key": key}
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("valid", False)
        else:
            # This logs the error to your Streamlit Cloud logs for debugging
            print(f"Lemon Squeezy API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

# 3. Sidebar Authentication Gate
with st.sidebar:
    st.header("Agency Authentication")
    user_key = st.text_input("Enter License Key", type="password", help="Enter your 150-audit license key")
    
    authenticated = False
    if user_key:
        if verify_license(user_key):
            st.success("✅ PRO License Active")
            st.info("🚀 150-Audit Agency License Loaded")
            authenticated = True
        else:
            st.error("❌ Invalid License Key")
            st.write("Check if you are in **Test Mode** or if the key has expired.")
    else:
        st.warning("Locked: License Required")

# 4. Main Application Logic
if authenticated:
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("Website URL", placeholder="https://vanmarlending.com")
    with col2:
        niche = st.text_input("Business Niche", placeholder="e.g., Mortgage Broker")

    if st.button("Generate Professional AI Audit"):
        if not target_url or not niche:
            st.warning("Please provide both a URL and a Niche.")
        else:
            # Initialize Gemini with Safety Bypass
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # This prevents the 'Invalid operation' error in sensitive niches like finance
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
            
            with st.spinner("Analyzing Site for GEO Gaps..."):
                try:
                    prompt = (
                        f"Act as a GEO (Generative Engine Optimization) expert. "
                        f"Audit {target_url} for the '{niche}' niche. "
                        f"1. Identify missing 'Atomic Answers' for AI search. "
                        f"2. Suggest specific JSON-LD schema improvements. "
                        f"3. Rank the site's AI-readiness from 1-10."
                    )
                    response = model.generate_content(prompt)
                    
                    # Display results
                    st.divider()
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"AI Generation Error: {str(e)}")
                    st.info("Tip: If the error persists, try a different niche or check your Google API quota.")

# 5. Footer
st.divider()
st.caption("Powered by Limon Media © 2026 | Built for the Generative Search Era")
