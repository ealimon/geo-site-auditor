import streamlit as st
import requests
import google.generativeai as genai

# --- 1. CONFIGURATION & SECRETS ---
# These must be set in your Streamlit Cloud "Secrets" dashboard
try:
    LEMON_API_KEY = st.secrets["LEMON_API_KEY"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Missing Secrets! Please add LEMON_API_KEY and GOOGLE_API_KEY to Streamlit Settings.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. LICENSE VALIDATION LOGIC ---
def check_license(key):
    """Verifies key and checks if 10-audit limit is reached."""
    url = "https://api.lemonsqueezy.com/v1/licenses/validate"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {LEMON_API_KEY}"
    }
    data = {"license_key": key}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        res_data = response.json()
        
        if res_data.get("valid"):
            # 'activation_usage' tracks how many times the audit has run
            usage = res_data.get("license_key", {}).get("activation_usage", 0)
            if usage >= 10:
                return False, "🚫 10/10 Credits Used. Please purchase a new license at Limon.media."
            return True, usage
        return False, "❌ Invalid License Key. Please check your email."
    except Exception as e:
        return False, f"⚠️ Connection Error: {str(e)}"

def increment_usage(key):
    """Signals Lemon Squeezy to count this as one audit used."""
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    headers = {"Accept": "application/json"}
    data = {"license_key": key, "instance_name": "GEO_Audit_Run"}
    requests.post(url, headers=headers, json=data)

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Limon AI | GEO Auditor", page_icon="🍋")

with st.sidebar:
    st.image("https://static.wixstatic.com/media/366f24_5ac147ad72ce4d5ca4736e59488eb340~mv2.webp")
    st.title("License Access")
    user_key = st.text_input("Enter License Key", type="password", help="Found in your Lemon Squeezy receipt")
    
    if user_key:
        is_valid, status_msg = check_license(user_key)
        if is_valid:
            st.success(f"Verified: {10 - status_msg} Audits Remaining")
        else:
            st.error(status_msg)
            st.stop()
    else:
        st.info("Enter your key to unlock the tool.")
        st.stop()

# --- 4. AUDIT INTERFACE ---
st.title("🍋 AI: GEO Site Auditor")
st.markdown("Analyze your site's visibility for AI search engines like Google Gemini and Perplexity.")

target_url = st.text_input("Website URL", placeholder="https://www.yourlawfirm.com")

if st.button("Run Smart Audit"):
    if target_url:
        with st.spinner("Gemini is analyzing site structure and factual density..."):
            # The AI Instructions
            prompt = f"""
            Act as a GEO (Generative Engine Optimization) expert. 
            Audit the following URL for AI search visibility: {target_url}.
            1. Provide a 'GEO Readiness Score' from 1-100.
            2. Write a 50-word 'Atomic Answer' optimized for LLM citations.
            3. Identify 3 specific content gaps to help this site rank in AI Overviews.
            """
            
            try:
                response = model.generate_content(prompt)
                increment_usage(user_key) # Deduct 1 credit
                
                st.divider()
                st.subheader("Audit Results")
                st.markdown(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"AI Analysis failed: {str(e)}")
    else:
        st.warning("Please enter a URL to analyze.")
