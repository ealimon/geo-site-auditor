import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- 1. SET UP THE USER INTERFACE ---
st.set_page_config(page_title="Limon Media GEO Auditor", page_icon="🚀")
st.title("🌐 AI Overview (GEO) Auditor")
st.subheader("Optimize your site for the AI Search Era")

# --- 2. INPUT AREA ---
url = st.text_input("Enter your website URL (e.g., https://example.com):")
analyze_button = st.button("Run AI Audit")

if analyze_button and url:
    try:
        # --- 3. SCRAPE THE WEBSITE ---
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        
        st.write("---")
        st.success(f"Successfully scanned: {url}")

        # --- 4. THE AUDIT LOGIC ---
        col1, col2 = st.columns(2)
        
        # Check for 'Atomic Answer' (Short paragraphs near headers)
        headers = soup.find_all(['h1', 'h2'])
        has_atomic = any(len(h.find_next('p').text.split()) < 60 for h in headers if h.find_next('p'))
        
        # Check for Schema Markup
        has_schema = "application/ld+json" in response.text

        # --- 5. DISPLAY RESULTS ---
        with col1:
            st.metric(label="GEO Readiness Score", value="75%" if has_atomic else "40%")
            
        with col2:
            st.write("**Quick Checks:**")
            st.write("✅ Schema Detected" if has_schema else "❌ No Schema Found")
            st.write("✅ Atomic Answer Found" if has_atomic else "❌ Needs 'TL;DR' Summary")

        st.info("**Strategy Suggestion:** Add a 50-word summary directly under your main H2 heading to increase your chances of appearing in AI Overviews.")

    except Exception as e:
        st.error(f"Could not scan site. Please check the URL. Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Powered by **Limon Media Store**")
