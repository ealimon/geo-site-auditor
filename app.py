import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- 1. CONFIGURATION & BRAIN SETUP ---
# Pulling keys from Streamlit Secrets for security
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Error: GEMINI_API_KEY not found in Streamlit Secrets.")

# Lemon Squeezy API Endpoint
LEMON_API_URL = "https://api.lemonsqueezy.com/v1/licenses/validate"

# --- 2. ADVANCED LICENSE LOGIC ---
def is_license_valid(key):
    """Checks the key against Lemon Squeezy servers."""
    try:
        # We send the key to Lemon Squeezy to see if it's active
        response = requests.post(
            LEMON_API_URL,
            data={"license_key": key},
            headers={"Accept": "application/json"}
        )
        data = response.json()
        
        # Returns True only if the key is valid and not expired/disabled
        return data.get("valid", False)
    except Exception as e:
        st.sidebar.error(f"Validation Error: {e}")
        return False

# --- 3. THE LOCK SCREEN (USER INTERFACE) ---
st.set_page_config(page_title="Limon AI: GEO Auditor", page_icon="🚀", layout="centered")

# Custom Branding CSS
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .stButton>button { background-color: #8cc63f; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Show Lock Screen if not logged in
if not st.session_state["authenticated"]:
    st.image("https://limon.media/logo.png", width=200) # Replace with your actual logo URL
    st.title("🔐 Unlock Your GEO Auditor")
    st.write("Please enter your license key from the **Limon Media Store** to continue.")
    
    user_key = st.text_input("License Key", type="password", placeholder="Paste your key here...")
    
    if st.button("Unlock Now"):
        with st.spinner("Verifying license..."):
            if is_license_valid(user_key):
                st.session_state["authenticated"] = True
                st.success("Success! Access Granted.")
                st.rerun()
            else:
                st.error("Invalid License Key. Please check your email or visit Limon.Media.")
    
    st.info("Don't have a key? [Get your access here](https://Limon.Media)")
    st.stop() # Blocks the rest of the app

# --- 4. THE AUDITOR (ONLY RUNS IF UNLOCKED) ---
st.title("🌐 Limon AI: GEO Site Auditor")
st.sidebar.button("Log Out", on_click=lambda: st.session_state.update({"authenticated": False}))

url = st.text_input("Enter website URL to audit:", placeholder="https://example.com")

def get_ai_audit(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Act as an SEO expert. Analyze this site for GEO (AI Overviews). Provide a score 1-100 and 3 tips: {text[:5000]}"
    return model.generate_content(prompt).text

if st.button("Run Smart Audit") and url:
    with st.spinner("Gemini is analyzing your content..."):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            report = get_ai_audit(soup.get_text())
            st.markdown(report)
        except Exception as e:
            st.error(f"Could not scan site: {e}")
