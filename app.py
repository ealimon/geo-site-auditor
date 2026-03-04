import streamlit as st
import google.generativeai as genai
import requests

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { opacity: 0.95; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("GEO Auditor PRO")

# 2. Updated License Verification (POST Method)
def verify_license(key):
    """
    Validates the license key against the Lemon Squeezy API.
    Uses POST to ensure compatibility with modern App Tokens.
    """
    try:
        # Pulls the Live API Key from your Streamlit Secrets
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"]
        
        url = "https://api.lemonsqueezy.com/v1/license-keys/validate"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }
        
        # Body of the request
        payload = {"license_key": key}
        
        # Perform the check
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            # Returns True only if 'valid' is true in the response
            return data.get("valid", False)
        else:
            # This will show up in your Streamlit 'Manage App' logs
            print(f"Lemon Squeezy API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Auth System Error: {e}")
        return False

# 3. Sidebar Authentication
with st.sidebar:
    st.header("Agency Authentication")
    st.info("Enter your PRO license key received via email to unlock the auditor.")
    
    user_key = st.text_input("Enter License Key", type="password", help="Example: 5F96D08C-...")
    
    authenticated = False
    if user_key:
        with st.spinner("Verifying License..."):
            if verify_license(user_key):
                st.success("PRO License Active")
                authenticated = True
            else:
                st.error("Invalid License Key")
                st.write("Ensure your store is in **Live Mode** and you are using a **Live Key**.")
    else:
        st.warning("License Required to proceed.")

# 4. Main Application Logic
if authenticated:
    st.subheader("Run New GEO Audit")
    col1, col2 = st.columns(2)
    
    with col1:
        target_url = st.text_input("Website URL", placeholder="https://example.com")
    with col2:
        niche = st.text_input("Business Niche", placeholder="e.g., Mortgage Broker in Austin")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please enter both a URL and a Niche.")
        else:
            try:
                # Configure Google AI
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                
                # Professional Safety Settings
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety)
                
                with st.spinner(f"Analyzing {target_url} for AI search visibility..."):
                    prompt = f"""
                    Act as a Senior SEO & GEO Specialist. 
                    Perform a professional Generative Engine Optimization (GEO) audit for {target_url} 
                    specializing in the {niche} niche. 
                    Identify content gaps for Gemini, Perplexity, and ChatGPT Search.
                    """
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"AI Generation Error: {e}")
                st.info("Check your GOOGLE_API_KEY in Streamlit Secrets.")

else:
    # This shows if they haven't entered a valid key yet
    st.image("https://via.placeholder.com/800x400.png?text=License+Required+to+Unlock+GEO+Auditor", use_container_width=True)

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
