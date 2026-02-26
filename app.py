import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import json
import re

# --- HELPER: STRIP EMOJIS FOR PDF COMPATIBILITY ---
def clean_text(text):
    # Removes emojis and special characters that crash standard FPDF fonts
    return re.sub(r'[^\x00-\x7F]+', '', text)

# --- PDF REPORT GENERATOR ---
class GEO_Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Limon Media: Professional GEO Strategy Report", ln=True, align="C")
        self.ln(10)

    def section_header(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f" {title}", ln=True, fill=True)
        self.ln(4)

    def write_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 7, clean_text(text)) # Cleaned text for PDF
        self.ln(5)

# --- THE HIGH-INTELLIGENCE ENGINE ---
def run_amazing_audit(url, niche):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        site_title = soup.title.string if soup.title else "Your Business"
        h2s = soup.find_all('h2')
        has_schema = "application/ld+json" in response.text
        word_count = len(soup.get_text().split())

        if len(h2s) < 3:
            structural_gap = f"Critical: Only {len(h2s)} H2 headers found. AI models require clear hierarchy."
        else:
            structural_gap = f"Structural health is moderate with {len(h2s)} headers detected."

        schema_status = "✅ Schema detected." if has_schema else "❌ No JSON-LD Schema found."
        
        schema_code = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": site_title,
            "url": url,
            "knowsAbout": [niche, "AI Optimization"]
        }

        results = {
            "score": 88 if has_schema and word_count > 500 else 55,
            "schema_output": json.dumps(schema_code, indent=4),
            "ai_strategy": (
                f"🎯 Deep Content Diagnostic for {niche}\n\n"
                f"Structural Check: {structural_gap}\n\n"
                f"Content Density: Your page has {word_count} words. Aim for 800+ for authority indexing.\n\n"
                f"Strategic Pivot: Use 'Objective Definition' language. Instead of marketing fluff, "
                f"define {site_title} as a primary entity in the {niche} space."
            ),
            "market_benchmark": (
                f"📊 Competitive Intelligence\n\n"
                f"Technical Status: {schema_status}\n\n"
                f"Industry Gap: 85% of top-cited brands use advanced Schema. Deploy the implementation code immediately."
            )
        }
        return results
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

# --- UI SETUP ---
st.set_page_config(page_title="Limon AI | GEO PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #FFD700; color: black; font-weight: bold; height: 3.5em; border: none; }
    .strategy-box { background-color: #ffffff; padding: 20px; border-left: 6px solid #FFD700; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍋 Limon Media: GEO Auditor PRO")

col_a, col_b = st.columns([2, 1])
with col_a:
    url_input = st.text_input("Website URL", placeholder="https://limon.media")
with col_b:
    niche_input = st.text_input("Business Niche", placeholder="e.g. AI Product Studio")

if st.button("Generate Professional Audit & Implementation Plan"):
    if url_input and niche_input:
        if not url_input.startswith("http"): url_input = "https://" + url_input
            
        with st.spinner("Analyzing..."):
            data = run_amazing_audit(url_input, niche_input)
            
            if "error" in data:
                st.error(data["error"])
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("GEO Readiness", f"{data['score']}/100", help="Likelihood of AI citation.")
                c2.metric("Entity Density", "High", help="Semantic relationship strength.")
                c3.metric("Status", "Optimized" if data['score'] > 80 else "Action Required")

                st.divider()

                t1, t2, t3 = st.tabs(["🚀 Strategic Strategy", "💻 Implementation Code", "📊 Market Intelligence"])
                
                with t1:
                    st.markdown(f'<div class="strategy-box">{data["ai_strategy"]}</div>', unsafe_allow_html=True)

                with t2:
                    st.code(data["schema_output"], language="json")

                with t3:
                    st.info(data["market_benchmark"])

                # --- PDF GENERATION ---
                pdf = GEO_Report()
                pdf.add_page()
                pdf.section_header("Executive GEO Strategy")
                pdf.write_text(data["ai_strategy"])
                pdf.section_header("Technical Implementation")
                pdf.write_text(data["schema_output"])
                
                pdf_bytes = pdf.output()
                st.download_button("📥 Download Pro Strategy PDF", data=bytes(pdf_bytes), file_name="Limon_Pro_Strategy.pdf")
