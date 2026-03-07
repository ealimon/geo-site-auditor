import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="GEO Auditor PRO | Limon Media", page_icon="🍋", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { background-color: #FFD700; color: black; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. CORE LOGIC: THE UNIVERSAL ENGINE
def run_geo_audit(url, niche):
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Using the standard model name to avoid 404 errors
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"You are a Senior GEO Strategist. Perform an audit for: {url} in the {niche} niche. "
            "\n\nFormat your response as follows:"
            "\n1. **AI Sentiment Analysis**"
            "\n2. **Information Density**"
            "\n3. **Citation Potential**"
            "\n4. **Top 3 Action Items**"
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return str(e)

# 3. SIDEBAR
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.divider()
    st.markdown("#### **Need an Expert?**")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")
    st.divider()
    st.caption("© 2026 Limon Media")

# 4. MAIN INTERFACE
st.title("GEO Auditor PRO")
target_url = st.text_input("Website URL", placeholder="https://yourbrand.com")
niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate")

if st.button("🚀 Run AI GEO Audit"):
    if not target_url or not niche:
        st.warning("Please enter both fields.")
    else:
        with st.spinner("Analyzing..."):
            result = run_geo_audit(target_url, niche)
            
            # Handle the "Wait" vs "Broken" errors
            if "429" in result:
                st.error("🍋 **Quota Full.** Google's free tier is busy. Please wait 60 seconds.")
            elif "404" in result:
                st.error("🍋 **Connection Error.** Please try again in a moment.")
            else:
                st.success("Audit Complete!")
                st.markdown(result)
                st.divider()
                st.markdown("### 🍋 Want to dominate AI Search?")
                st.link_button("Contact Limon Media", "https://www.limon.media/contact")
