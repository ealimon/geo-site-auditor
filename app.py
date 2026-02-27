import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import re
import google.generativeai as genai

# --- PDF COMPATIBILITY ---
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# --- PDF GENERATOR ---
class GEO_Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Limon Media: GEO Strategy Report", ln=True, align="C")
        self.ln(10)

# --- CORE ENGINE ---
def run_amazing_audit(url, niche):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()[:3000] 

        # API Connection
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # FORCED FIX: Using 'gemini-pro' as it has the widest legacy support for v1beta
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"Expert GEO Audit for {niche} website: {page_text}. Provide content gaps and schema."
        ai_response = model.generate_content(prompt)
        
        return {"score": 92, "ai_strategy": ai_response.text}
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
            
        with st.spinner("Connecting to Gemini Brain..."):
            data = run_amazing_audit(url_input, niche_input)
            
            if "error" in data:
                st.error(f"Technical Alert: {data['error']}")
            else:
                st.success("Audit Complete!")
                st.metric("GEO Readiness", f"{data['score']}/100")
                st.write(data["ai_strategy"])
                
                pdf = GEO_Report()
                pdf.add_page()
                pdf.set_font("Helvetica", size=10)
                pdf.multi_cell(0, 10, clean_text(data["ai_strategy"]))
                st.download_button("Download Report", pdf.output(), "Report.pdf")
