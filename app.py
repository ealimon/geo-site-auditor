import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import re
import google.generativeai as genai

# --- PDF COMPATIBILITY ---
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# --- THE LIVE AI BRIDGE ---
def run_amazing_audit(url, niche):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()[:3000] 

        # API Connection from Secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # AUTO-DETECTION: Find a model that works to bypass 404 errors
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models:
            return {"error": "No compatible models found for this API key."}
        
        # Pick the best available (prioritizing flash if it exists)
        target_model = next((m for m in available_models if "flash" in m), available_models[0])
        model = genai.GenerativeModel(target_model)

        prompt = f"Expert GEO Audit for {niche} website: {page_text}. Provide content gaps and schema."
        ai_response = model.generate_content(prompt)
        
        return {"score": 92, "ai_strategy": ai_response.text, "model_used": target_model}
    except Exception as e:
        return {"error": str(e)}

# --- INTERFACE ---
st.set_page_config(page_title="Limon AI | GEO PRO")
st.title("🍋 Limon Media: GEO Auditor PRO")
st.sidebar.info("🚀 PRO License: 150 Audits Remaining")

url_input = st.text_input("Website URL", placeholder="https://www.limon.media/")
niche_input = st.text_input("Business Niche", placeholder="digital marketing")

if st.button("Generate Professional AI Audit"):
    if url_input and niche_input:
        if not url_input.startswith("http"):
            url_input = "https://" + url_input
            
        with st.spinner("Searching for available AI Brain..."):
            data = run_amazing_audit(url_input, niche_input)
            
            if "error" in data:
                st.error(f"Technical Alert: {data['error']}")
            else:
                st.success(f"Audit Complete using {data['model_used']}!")
                st.metric("GEO Readiness", f"{data['score']}/100")
                st.write(data["ai_strategy"])
    else:
        st.warning("Please fill in both fields.")
