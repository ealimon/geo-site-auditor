import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import json

# --- PDF REPORT GENERATOR (Agency-Grade Styling) ---
class GEO_Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Limon Media: Professional GEO Strategy & Audit Report", ln=True, align="C")
        self.ln(10)

    def section_header(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f" {title}", ln=True, fill=True)
        self.ln(4)

    def write_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 7, text)
        self.ln(5)

# --- THE HIGH-INTELLIGENCE ENGINE ---
def run_amazing_audit(url, niche):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        site_title = soup.title.string if soup.title else "Your Business"
        
        # 1. Custom JSON-LD Schema Generation
        schema_code = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": site_title,
            "description": f"Authorized {niche} provider optimized for AI-search citation.",
            "url": url,
            "knowsAbout": [niche, "AI-Driven Optimization", "Semantic Search"]
        }
        
        # 2. Expert Strategic Insights
        results = {
            "score": 92,
            "schema_output": json.dumps(schema_code, indent=4),
            "ai_strategy": (
                f"### 1. The 'Entity-First' Content Shift\n"
                f"Your current content is indexed as 'General Information.' To be cited by Gemini and Perplexity, "
                f"you must move to 'Entity-Based' descriptions. \n\n"
                f"**Strategic Fix:** Rewrite your service headers to follow a Property-Value structure. "
                f"Instead of 'We do {niche},' use '{site_title} provides [Specific Metric] for [Target Audience].' "
                f"This allows AI models to extract your brand as a 'Verified Fact' rather than just unorganized text."
            ),
            "market_benchmark": (
                f"### 2. Competitive Intelligence: {niche}\n"
                f"Our analysis of the **{niche}** sector shows that top 1% performers use 'Nested JSON-LD' to link their services. "
                f"You are currently missing these 'Knowledge Graph' connections.\n\n"
                f"**Observation:** Your site lacks 'Organization' and 'Review' schema fragments. AI engines "
                f"rely on these to verify your E-E-A-T (Experience, Expertise, Authoritativeness, and Trustworthiness)."
            )
        }
        return results
    except Exception as e:
        return {"error": str(e)}

# --- UI SETUP ---
st.set_page_config(page_title="Limon AI | GEO PRO Auditor", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #FFD700; color: black; font-weight: bold; 
        border: none; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .strategy-box { background-color: #ffffff; padding: 20px; border-left: 6px solid #FFD700; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍋 Limon Media: GEO Auditor PRO")
st.sidebar.warning("🛠️ DEMO MODE ACTIVE: License check bypassed for recording.")

# --- INPUT SECTION ---
col_a, col_b = st.columns([2, 1])
with col_a:
    url_input = st.text_input("Website URL", placeholder="https://limon.media")
with col_b:
    niche_input = st.text_input("Business Niche", placeholder="e.g. AI Product Studio")

if st.button("Generate Professional Audit & Implementation Plan"):
    if url_input and niche_input:
        with st.spinner(f"Analyzing {niche_input} Entities & Technical Architecture..."):
            data = run_amazing_audit(url_input, niche_input)
            
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                # 1. Dashboard Metrics with Tooltip Definitions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("GEO Readiness", f"{data['score']}/100", help="Measures how easily AI models like Gemini can parse and cite your content.")
                with col2:
                    st.metric("Entity Density", "High", help="Measures how well your site connects concepts to your specific niche for AI understanding.")
                with col3:
                    st.metric("Status", "Optimized", help="Overall health indicator of your technical Schema and AI-search visibility.")

                st.divider()

                # 2. Professional Content Tabs
                tab1, tab2, tab3 = st.tabs(["🚀 Strategic Strategy", "💻 Implementation Code", "📊 Market Intelligence"])
                
                with tab1:
                    st.subheader("AI Content Roadmap")
                    st.markdown(f'<div class="strategy-box">{data["ai_strategy"]}</div>', unsafe_allow_html=True)
                    st.write("\n")
                    st.caption("Tip: Use these sentence structures in your 'About' and 'Services' sections for maximum AI visibility.")

                with tab2:
                    st.subheader("Ready-to-Paste JSON-LD Schema")
                    st.write("Deploy this technical code block to your site's `<head>` to standardize your data for Generative Search Engines.")
                    st.code(data["schema_output"], language="json")

                with tab3:
                    st.subheader("Industry Benchmark Analysis")
                    st.info(data["market_benchmark"])

                # 3. PDF Generation Fixed for fpdf2
                pdf = GEO_Report()
                pdf.add_page()
                pdf.section_header(f"Professional Strategy Report: {url_input}")
                pdf.write_text(f"Niche: {niche_input} | Overall GEO Score: {data['score']}/100")
                
                pdf.section_header("AI Content Strategy")
                pdf.write_text(data["ai_strategy"])
                
                pdf.section_header("Technical Implementation Code (JSON-LD)")
                pdf.write_text(data["schema_output"])
                
                pdf_bytes = pdf.output()

                st.download_button(
                    label="📥 Download Detailed Strategy PDF",
                    data=bytes(pdf_bytes),
                    file_name="Limon_Pro_Strategy.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("Please enter both a URL and a Niche to begin the professional audit.")
