import streamlit as st
import google.generativeai as genai
import requests
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="GEO Auditor PRO", layout="wide")
st.title("GEO Auditor PRO")

# 2. Working License Verification (The one that finally worked!)
def verify_license(license_key):
    try:
        api_key = st.secrets["LEMON_SQUEEZY_API_KEY"].strip().strip('"').strip("'")
        url = "https://api.lemonsqueezy.com/v1/licenses/validate"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
        payload = {"license_key": license_key}
        # Use data= for form-encoded delivery
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json().get("valid", False)
        return False
    except:
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
    target_url = st.text_input("Website URL", placeholder="https://limon.media")
    niche = st.text_input("Business Niche", placeholder="e.g., Digital Marketing")

    if st.button("Generate AI Audit"):
        if not target_url or not niche:
            st.warning("Please fill in both fields.")
        else:
            try:
                # Initialize Gemini
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                
                # THE FIX: Use 'gemini-1.5-flash' without the /models/ prefix 
                # to avoid the 404 error shown in your logs.
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("Analyzing Professional Audit..."):
                    prompt = f"Perform a professional GEO (Generative Engine Optimization) audit for {target_url} in the {niche} niche. Focus on AI search visibility."
                    response = model.generate_content(prompt)
                    
                    # Display Result
                    st.divider()
                    st.markdown(response.text)
                    
                    # PDF Generation Logic
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, f"GEO Audit for: {target_url}\nNiche: {niche}\n\n{response.text}")
                    
                    # Provide Download Button
                    st.download_button(
                        label="Download Audit as PDF",
                        data=pdf.output(dest='S'),
                        file_name=f"GEO_Audit_{target_url}.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")

st.divider()
st.caption("Powered by Limon Media © 2026 | All Rights Reserved")
