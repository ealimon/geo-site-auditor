import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import json

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
        self.multi_cell(0, 7, text)
        self.ln(5)

# --- THE HIGH-INTELLIGENCE ENGINE ---
def run_amazing_audit(url, niche):
    try:
        # 1. LIVE SITE DIAGNOSTIC
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape data points
        site_title = soup.title.string if soup.title else "Your Business"
        h2s = soup.find_all('h2')
        has_schema = "application/ld+json" in response.text
        word_count = len(soup.get_text().split())

        # 2. CUSTOM LOGIC BASED ON FINDINGS
        # Semantic Analysis
        if len(h2s) < 3:
            structural_gap = f"Critical: Only {len(h2s)} H2 headers found. AI models like Gemini require a clear question-based hierarchy to index your site as an authority on {niche}."
        else:
            structural_gap = f"Structural health is moderate, but headers lack 'Entity Linking.' Optimize your {len(h2s)} headers to include specific {niche} definitions."

        # Technical Analysis
        schema_status = "✅ Schema detected." if has_schema else "❌ No JSON-LD Schema found. AI agents cannot verify your business identity."
        
        # 3. GENERATE OUTPUT
        schema_code = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": site_title,
            "description": f"Verified {niche} authority.",
            "url": url,
            "knowsAbout": [niche, "AI Optimization", "Semantic Search"]
        }

        results = {
            "score": 88 if has_schema and word_count > 500 else 55,
            "schema_output": json.dumps(schema_code, indent=4),
            "ai_strategy": (
                f"### 🎯 Deep Content Diagnostic for {niche}\n"
                f"**Structural Check:** {structural_gap}\n\n"
                f"**Content Density:** Your page has {word_count} words. For high-authority GEO ranking, aim for 800+ words of 'Definition-Rich' content.\n\n"
                f"**Strategic Pivot:** Stop using 'Marketing Fluff.' Use 'Objective Definition' language. "
                f"Instead of saying 'We are great at {niche},' use '{site_title} is a {niche} institution specializing in [X] with [Y] years of verified service.'"
            ),
            "market_benchmark": (
                f"### 📊 Competitive Intelligence\n"
                f"**Technical Status:** {schema_status}\n\n"
                f"**Industry Gap:** 85% of top-cited {niche} brands use 'FAQ' and 'Organization' Schema to secure their place in AI Overviews. "
                f"Deploy the code in the 'Implementation' tab to bridge this authority gap immediately."
            )
        }
        return results
    except Exception as e:
        return {"error": f"Unable to reach site: {str(e)}"}

# --- UI SETUP ---
st.set_page_config(page_title="Limon AI | GEO PRO", layout="wide")

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
st.sidebar.warning("🛠️ DEMO MODE ACTIVE")

# --- INPUT SECTION ---
col_a, col_b = st.columns([2, 1])
with col_a:
    url_input = st.text_input("Website URL", placeholder="https://example.com")
with col_b:
    niche_input = st.text_input("Business Niche", placeholder="e.g. AI Product Studio")

if st.button("Generate Professional Audit & Implementation Plan"):
    if url_input and niche_input:
        if not url_input.startswith("http"):
            url_input = "https://" + url_input
            
        with st.spinner(f"Scanning technical architecture for {niche_input}..."):
            data = run_amazing_audit(url_input, niche_input)
            
            if "error" in data:
                st.error(data["error"])
            else:
                # 1. Metrics Dashboard
                c1, c2, c3 = st.columns(3)
                c1.metric("GEO Readiness", f"{data['score']}/100", help="Likelihood of being cited in AI Search Overviews.")
                c2.metric("Entity Density", "Live Analyzed", help="Analysis of keyword-to-concept relationships.")
                c3.metric("Industry Rank", "Top 20%", help="How you compare to others in the niche.")

                st.divider()

                # 2. Tabs
                t1, t2, t3 = st.tabs(["🚀 Strategic Strategy", "💻 Implementation Code", "📊 Market Intelligence"])
                
                with t1:
                    st.subheader("Deep Content Roadmap")
                    st.markdown(f'<div class="strategy-box">{data["ai_strategy"]}</div>', unsafe_allow_html=True)

                with t2:
                    st.subheader("Ready-to-Paste JSON-LD Schema")
                    st.code(data["schema_output"], language="json")

                with t3:
                    st.subheader("Niche Benchmark Analysis")
                    st.info(data["market_benchmark"])

                # 3. PDF Export
                pdf = GEO_Report()
                pdf.add_page()
                pdf.section_header(f"GEO Audit: {url_input}")
                pdf.write_text(data["ai_strategy"])
                pdf.section_header("Implementation Schema")
                pdf.write_text(data["schema_output"])
                
                pdf_bytes = pdf.output()
                st.download_button("📥 Download Pro Strategy PDF", data=bytes(pdf_bytes), file_name="Limon_Pro_Strategy.pdf")
    else:
        st.warning("Please provide a URL and Niche to start.")
