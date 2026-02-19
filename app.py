import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- 1. SETUP THE BRAIN ---
# We will pull the API key from Streamlit Secrets for security
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please add it to Streamlit Secrets.")

def get_ai_audit(website_text):
    model = gemini-flash-latest
    prompt = f"""
    Act as a SEO expert specialized in AI Overviews (GEO). 
    Analyze the following website content and provide:
    1. A 'GEO Score' from 1-100.
    2. Three specific improvements to help this site appear in AI Overviews.
    3. An 'Atomic Answer' (a 50-word summary) they should add to their homepage.
    
    Website Content: {website_text[:5000]} 
    """
    response = model.generate_content(prompt)
    return response.text

# --- 2. THE USER INTERFACE ---
st.set_page_config(page_title="Limon Media AI Auditor", page_icon="🚀")
st.title("🌐 AI Overview (GEO) Auditor")
st.write("Powered by **Limon Media**")

url = st.text_input("Enter website URL:")
if st.button("Run Smart Audit") and url:
    with st.spinner("Gemini is analyzing your site..."):
        try:
            # Scrape site
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            clean_text = soup.get_text()

            # Get AI Analysis
            report = get_ai_audit(clean_text)
            
            st.success("Analysis Complete!")
            st.markdown(report)
            
        except Exception as e:
            st.error(f"Error: {e}")
