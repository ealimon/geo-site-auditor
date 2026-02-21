import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- 1. CONFIGURATION & BRAIN SETUP ---
# Securely pulling keys from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    # Using 'gemini-1.5-flash' as it is the most stable production model currently
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Error: GEMINI_API_KEY not found in Streamlit Secrets.")

# Lemon Squeezy API Endpoint for license validation
LEMON_API_URL = "https://api.lemonsqueezy.com/v1/licenses/validate"

# --- 2. ADVANCED LICENSE LOGIC ---
def is_license_valid(key):
    """Checks the key against Lemon Squeezy servers."""
    try:
        response = requests.post(
            LEMON_API_URL,
            data={"license_key": key},
            headers={"Accept": "application/json"}
        )
        data = response.json()
        # Returns True only if the key is valid in your store
        return data.get("valid", False)
    except Exception as e:
        st.sidebar.error(f"Validation Error: {e}")
        return False

# --- 3. THE LOCK SCREEN (USER INTERFACE) ---
st.set_page_config(page_title="Limon AI: GEO Auditor", page_icon="🚀", layout="centered")

# Custom Branding CSS to match your premium PDF guide
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .stButton>button { 
        background-color: #8cc63f; 
        color: white; 
        border-radius: 8px; 
        font-weight: bold;
        width: 100%;
    }
    .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Show Lock Screen if not logged in
if not st.session_state["authenticated"]:
    # FIXED: Using your provided Wix image address
    st.image("https://static.wixstatic.com/media/366f24_4d95e26872a648fcb875a7f8b3782abe~mv2.jpg/v1/fill/w_150,h_90,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/facebook.jpg", width=150)
    
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
    st.stop() 

# --- 4. THE AUDITOR (ONLY RUNS IF UNLOCKED) ---
st.title("🌐 Limon AI: GEO Site Auditor")
st.sidebar.title("Settings")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.rerun()

url = st.text_input("Enter website URL to audit:", placeholder="https://www.limon.media/")

def get_ai_audit(text):
    # Updated model name to 'gemini-1.5-flash' to match current API standards
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Act as a SEO expert specialized in AI Overviews (GEO). 
    Analyze the following website content and provide:
    1. A 'GEO Score' from 1-100.
    2. Three specific improvements to help this site appear in AI Overviews.
    3. An 'Atomic Answer' (a 50-word summary) they should add to their homepage.
    
    Website Content: {text[:5000]} 
    """
    response = model.generate_content(prompt)
    return response.text

if st.button("Run Smart Audit") and url:
    with st.spinner("Gemini is analyzing your site..."):
        try:
            # Scrape site content
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            clean_text = soup.get_text()

            # Get AI Analysis
            report = get_ai_audit(clean_text)
            
            st.success("Analysis Complete!")
            st.markdown(report)
            
        except Exception as e:
            st.error(f"Error: Could not scan the site. {e}")
