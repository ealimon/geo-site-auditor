import streamlit as st
import requests
import google.generativeai as genai

# --- 1. CONFIGURATION & SECRETS ---
# Ensure these are added to your Streamlit 'Secrets' dashboard
LEMON_API_KEY = st.secrets["LEMON_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
PRODUCT_ID = "YOUR_LEMON_SQUEEZY_PRODUCT_ID" # Replace with yours

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. LICENSE VALIDATION LOGIC ---
def check_license(key):
    """Verifies key and checks if audit credits (10) are exhausted."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {"Accept": "application/json"}
    data = {"license_key": key}
    
    try:
        response = requests.post(url, headers=headers, data=data)
        res_data = response.json()
        
        if res_data.get("valid"):
            usage = res_data["license_key"]["activation_usage"]
            # We treat 'activations' as 'audit credits' for this $19.95 model
            if usage >= 10:
                return False, f"🚫 10/10 Credits Used. [Top up here](https://limon.media)"
            return True, usage
        return False, "❌ Invalid License Key."
    except Exception:
        return False, "⚠️ Connection Error. Please try again."

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Limon AI | GEO Auditor", page_icon="🍋")

# Sidebar for License Key
with st.sidebar:
    st.image("https://static.wixstatic.com/media/366f24_5ac147ad72ce4d5ca4736e59488eb340~mv2.webp")
    user_key = st.text_input("Enter License Key", type="password")
    
    if user_key:
        is_valid, status = check_license(user_key)
        if is_valid:
            st.success(f"Verified: {10 - status} Audits Remaining")
        else:
            st.error(status)
            st.stop() # Prevents app from running without valid key
    else:
        st.info("Please enter your key to unlock the tool.")
        st.stop()

# Main Tool Interface
st.title("🍋 AI: GEO Site Auditor")
target_url = st.text_input("Enter Website URL to Audit", placeholder="https://example.com")

if st.button("Run Smart Audit"):
    if target_url:
        with st.spinner("Gemini is analyzing AI visibility..."):
            # Sample Gemini Prompt for GEO Audit
            prompt = f"Perform a GEO (Generative Engine Optimization) audit for {target_url}. Provide a 1-100 score, a 50-word Atomic Answer, and identify 3 content gaps for AI search."
            response = model.generate_content(prompt)
            
            st.subheader("Audit Results")
            st.write(response.text)
            
            # NOTE: To permanently increment usage, you must 'Activate' the key via API
            # requests.post('https://api.lemonsqueezy.com/v1/licenses/activate', data={'license_key': user_key, 'instance_name': 'Audit_Run'})
    else:
        st.warning("Please enter a URL.")
