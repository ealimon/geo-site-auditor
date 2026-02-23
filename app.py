import streamlit as st
import requests
import google.generativeai as genai

# --- CONFIGURATION & SECRETS ---
# Add these to your Streamlit "Secrets" dashboard
try:
    LEMON_API_KEY = st.secrets["LEMON_API_KEY"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add your API keys to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- LICENSE VALIDATION ---
def validate_lemon_license(license_key):
    """Checks if key is valid and has remaining activations."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {LEMON_API_KEY}"
    }
    # We send the license key to Lemon Squeezy to check its status
    response = requests.post(url, headers=headers, json={"license_key": license_key})
    data = response.json()

    if data.get("valid") is True:
        # 'activation_usage' counts how many times the audit has been run
        usage = data.get("license_key", {}).get("activation_usage", 0)
        limit = data.get("meta", {}).get("activation_limit", 10)
        
        if usage >= limit:
            return False, f"🚫 Credits Exhausted ({usage}/{limit}). Please buy a new pack at Limon.media."
        return True, usage
    
    return False, "❌ Invalid License Key. Please check your email receipt."

def activate_audit_use(license_key):
    """Calls the API to increment the usage count by 1."""
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    headers = {"Accept": "application/json"}
    # This 'activates' one instance, essentially deducting 1 credit
    requests.post(url, headers=headers, json={
        "license_key": license_key,
        "instance_name": "GEO_Audit_Run"
    })

# --- USER INTERFACE ---
st.set_page_config(page_title="Limon AI | GEO Auditor", page_icon="🍋")

with st.sidebar:
    st.image("https://static.wixstatic.com/media/366f24_5ac147ad72ce4d5ca4736e59488eb340~mv2.webp")
    st.title("License Access")
    user_key = st.text_input("Enter License Key", type="password")
    
    if user_key:
        valid, status = validate_lemon_license(user_key)
        if not valid:
            st.error(status)
            st.stop()
        else:
            st.success(f"Verified: {10 - status} Audits Remaining")
    else:
        st.info("Enter your key to unlock.")
        st.stop()

# --- THE AUDITOR ---
st.title("🍋 AI: GEO Site Auditor")
target_url = st.text_input("Enter Website URL to Audit", placeholder="https://example.com")

if st.button("Run Smart Audit"):
    if target_url:
        with st.spinner("Analyzing site structure for AI Search..."):
            prompt = f"Audit this URL for AI search engine visibility (GEO): {target_url}. Provide a readiness score and 3 content gaps."
            
            try:
                response = model.generate_content(prompt)
                # Success! Now deduct the credit
                activate_audit_use(user_key)
                
                st.subheader("Results")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
