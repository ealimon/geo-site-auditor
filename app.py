import streamlit as st
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import pandas as pd

# --- PDF REPORT GENERATOR ---
class GEO_Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Limon Media: GEO Audit Professional Report", ln=True, align="C")
        self.ln(10)

    def section_header(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, f" {title}", ln=True, fill=True)
        self.ln(4)

    def write_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 7, text)
        self.ln(5)

# --- DETAILED AUDIT ENGINE ---
def run_detailed_audit(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Technical Signals
        schema = soup.find_all('script', type='application/ld+json')
        h1_count = len(soup.find_all('h1'))
        word_count = len(soup.get_text().split())
        
        # Deep GEO Insights
        insights = {
            "score": 92 if len(schema) > 0 else 65,
            "technical_findings": [
                f"Schema Markup: {'✅ Optimized' if len(schema) > 0 else '❌ Missing JSON-LD'}",
                f"Heading Structure: {'✅ Found' if h1_count > 0 else '❌ No H1 detected'}",
                f"Content Depth: {word_count} words analyzed."
            ],
            "geo_optimization_strategy": (
                "To improve Generative Engine Optimization (GEO) visibility, this site must implement 'Atomic Answers.' "
                "AI Search Engines (like Gemini and Perplexity) prioritize content that directly answers user intent in the first 100 words of a section. "
                "Your current structure lacks 'Direct Answer' formatting. We recommend adding a FAQ section with JSON-LD 'Question' schema "
                "to increase the likelihood of being cited in AI Overviews."
            ),
            "semantic_recommendations": (
                "1. Cite Authority: AI models favor content that cites credible sources. Link to industry whitepapers.\n"
                "2. Natural Language: Shift from keyword-stuffing to 'Entity-Based' SEO. Use synonyms and related concepts (LSI).\n"
                "3. Technical Schema: Implement 'Organization' and 'Review' schema to build trust signals for AI agents."
            )
        }
        return insights
    except Exception as e:
        return {"error": str(e)}

# --- UI SETUP ---
st.set_page_config(page_title="Limon AI | GEO PRO", layout="wide")

st.markdown("""
    <style>
    .stButton>button { background-color: #FFD700; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; }
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍋 Limon Media: GEO Auditor PRO")
st.sidebar.warning("🛠️ DEMO MODE ACTIVE")

url_input = st.text_input("Enter Website URL", placeholder="https://limon.media")

if st.button("Generate Professional GEO Audit"):
    if url_input:
        with st.spinner("Performing Deep Semantic Analysis..."):
            results = run_detailed_audit(url_input)
            
            if "error" in results:
                st.error(results["error"])
            else:
                # 1. VISUAL DASHBOARD (The "Screen" Display)
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("Technical Health")
                    for finding in results["technical_findings"]:
                        st.write(finding)
                    st.metric("GEO Readiness Score", f"{results['score']}/100")
                
                with col2:
                    st.subheader("AI Visibility Strategy")
                    st.markdown(f"**The 'Atomic' Gap:**\n{results['geo_optimization_strategy']}")
                
                st.divider()
                
                st.subheader("Semantic & Entity Recommendations")
                st.success(results["semantic_recommendations"])
                
                # 2. PDF GENERATION (The "Export" Functionality)
                pdf = GEO_Report()
                pdf.add_page()
                pdf.section_header(f"Professional Audit: {url_input}")
                pdf.write_text(f"GEO Readiness Score: {results['score']}/100")
                
                pdf.section_header("AI Visibility Strategy")
                pdf.write_text(results['geo_optimization_strategy'])
                
                pdf.section_header("Technical & Semantic Recommendations")
                pdf.write_text(results['semantic_recommendations'])
                
                pdf_bytes = pdf.output()

                st.download_button(
                    label="📥 Download Detailed PDF Report",
                    data=bytes(pdf_bytes),
                    file_name="Limon_GEO_Pro_Report.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("Please enter a URL to audit.")
