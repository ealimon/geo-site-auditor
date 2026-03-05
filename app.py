import streamlit as st
import google.generativeai as genai
import requests
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Working License Verification (Lemon Squeezy)
def verify_license(license_key):
    try:
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"].strip().strip('"').strip("'")
        url = "https://api.lemonsqueezy.com/v1/licenses/validate"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
        payload = {"license_key": license_key}
        response = requests.post(url, headers=headers, data=payload)
        return response.json().get("valid", False) if response.status_code == 200 else False
    except:
        return False

# 3. NEW: Smart Model Selector (Prevents 404 Errors)
def get_best_model():
    """Finds the most modern 'flash' model available on your API key."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # List all models that support generating content
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list: Look for newest models first (3.0 -> 2.5 -> 1.5)
        for preferred in ['gemini-3-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']:
            for m in models:
                if preferred in m:
                    return m
        return models[0] # Fallback to whatever is available
    except Exception as e:
        return "gemini-1.5-flash" # Hard fallback

# 4. Sidebar Authentication
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

# 5. Main Application Logic
if authenticated:
    target_url = st.text_input("Website URL", placeholder="https://example.com")
    niche = st.text_input("Business Niche", placeholder="e.g., Dentist in London")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please fill in both fields.")
        else:
            try:
                # Dynamically get the model name
                model_name = get_best_model()
                model = genai.GenerativeModel(model_name)
                
                with st.spinner(f"Analyzing via {model_name}..."):
                    prompt = f"Professional GEO audit for {target_url} in the {niche} niche. Focus on AI search visibility."
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                    
                    # PDF Export
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    clean_text = response.text.replace("**", "").replace("#", "")
                    pdf.multi_cell(0, 10, f"GEO Audit: {target_url}\n\n{clean_text}")
                    st.download_button("Download PDF", pdf.output(dest='S'), f"Audit_{target_url}.pdf", "application/pdf")
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
