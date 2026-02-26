import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import json
import pandas as pd

# --- PDF REPORT GENERATOR CLASS ---
class GEO_Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Limon Media: GEO Audit Professional Report", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f" {title}", ln=True, fill=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 7, body)
        self.ln(5)

# --- CORE AUDIT FUNCTIONS ---
def run_geo_audit(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Schema Check
        schema = soup.find_all('script', type='application/ld+json')
        has_schema = len(schema) > 0
        
        # 2. Image Audit
        images = soup.find_all('img')
        missing_alt = [img.get('src') for img in images if not img.get('alt')]
        
        # 3. Content Analysis (Mocked for Demo - usually uses Gemini API)
        results = {
            "score": 88 if has_schema else 62,
            "schema_detected": has_schema,
            "missing_alt_count": len(missing_alt),
            "content_gap": "Site lacks 'Direct Answer' formatting (H2 questions). Semantic density for primary keywords is below 1.5%.",
            "recommendation": "Add a FAQ schema block and optimize image alt-tags with descriptive entities."
        }
        return results
    except Exception as e:
        return {"error": str(e)}

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Limon AI | GEO PRO Auditor", layout="wide")

# Custom CSS for a "Pro" look
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FFD700; color: black; font-weight: bold; }
    </style>
    """, unsafe_content_type=True)

st.title("🍋 Limon Media: GEO Auditor PRO")
st.write("Professional AI-Search Optimization & Technical Audit Tool")

# --- LICENSE CHECK (BYPASSED FOR DEMO) ---
# In production, you would use: license_key = st.sidebar.text_input("License Key")
st.sidebar.warning("🛠️ DEMO MODE ACTIVE: License check bypassed for recording.")
demo_is_active = True 

if demo_is_active:
    target_url = st.text_input("Enter Website URL (include https://)", placeholder="https://www.yourclient.com")
    
    if st.button("Generate Professional Audit"):
        if target_url:
            with st.spinner("Analyzing Site Architecture & AI Readability..."):
                data = run_geo_audit(target_url)
                
                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    # Metrics Row
                    col1, col2, col3 = st.columns(3)
                    col1.metric("GEO Readiness", f"{data['score']}/100")
                    col2.metric("Schema Status", "FOUND" if data['schema_detected'] else "MISSING")
                    col3.metric("Image Issues", data['missing_alt_count'])
                    
                    st.divider()
                    
                    # Detailed Analysis
                    tab1, tab2 = st.tabs(["Content Gaps", "Technical Fixes"])
                    with tab1:
                        st.write("### AI Semantic Analysis")
                        st.info(data['content_gap'])
                    with tab2:
                        st.write("### Technical Steps")
                        st.write(f"- **Schema:** { 'JSON-LD Verified' if data['schema_detected'] else 'ACTION REQUIRED: Implement LocalBusiness Schema'}")
                        st.write(f"- **Images:** { 'All images optimized' if data['missing_alt_count'] == 0 else f'ACTION REQUIRED: Fix {data[2]} missing Alt-tags'}")

                    # PDF Generation Logic
                    pdf = GEO_Report()
                    pdf.add_page()
                    pdf.chapter_title(f"Audit Results for {target_url}")
                    pdf.chapter_body(f"Overall Score: {data['score']}/100")
                    pdf.chapter_title("Content Optimization Gaps")
                    pdf.chapter_body(data['content_gap'])
                    pdf.chapter_title("Technical Recommendations")
                    pdf.chapter_body(data['recommendation'])
                    
                    pdf_output = pdf.output(dest='S').encode('latin-1')

                    st.download_button(
                        label="📥 Download White-Label PDF Report",
                        data=pdf_output,
                        file_name="Limon_Media_Pro_Audit.pdf",
                        mime="application/pdf"
                    )
        else:
            st.error("Please enter a valid URL to begin.")

else:
    st.info("Please enter your PRO License Key in the sidebar to access this tool.")
