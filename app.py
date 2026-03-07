import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="GEO Auditor PRO | Limon Media", 
    page_icon="🍋", 
    layout="wide"
)

# Custom CSS for the Limon Brand Aesthetic
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        background-color: #FFD700; 
        color: black; 
        border-radius: 8px; 
        border: none; 
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CORE LOGIC: THE STABLE ENGINE
def run_geo_audit(url, niche):
    try:
        # Configure the API with your Secret Key
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Using the exact stable model name to avoid 404/429 errors
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = (
            f"You are a Senior GEO Strategist. Perform an audit for: {url} in the {niche} niche. "
            "\n\nFormat your response as follows:"
            "\n1. **AI Sentiment Analysis** (How LLMs see you)"
            "\n2. **Information Density** (Is your site easy for AI to read?)"
            "\n3. **Citation Potential** (Will AI source you?)"
            "\n4. **Top 3 Action Items** to improve visibility."
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# 3. SIDEBAR
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.divider()
    st.markdown("### 🛠️ More Tools")
    st.write("🧪 *Internal Beta:* Local Maps LLM Optimizer")
    st.divider()
    st.markdown("#### **Need an Expert?**")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")

# 4. MAIN INTERFACE
st.title("GEO Auditor PRO")
st.markdown("Analyze how **AI Search Engines** perceive your brand in seconds.")

col1, col2 = st.columns(2)
with col1:
    target_url = st.text_input("Website URL", placeholder="https://yourbrand.com")
with col2:
    niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate")

st.divider()

if st.button("🚀 Run AI GEO Audit"):
    if not target_url or not niche:
        st.warning("Please enter both a URL and a Niche.")
    else:
        with st.spinner("Analyzing..."):
            result = run_geo_audit(target_url, niche)
            
            if "Error:" in result:
                if "429" in result:
                    st.error("🍋 **Quota Squeezed!** Google's free tier is busy. Please wait 60 seconds and try again.")
                else:
                    st.error(result)
            else:
                st.success("Audit Complete!")
                st.markdown(result)
                st.divider()
                # FIXED: Added missing closing parenthesis and quote below
                st.markdown("### 🍋 Want to dominate AI Search?")
                st.link_button("Contact Limon Media", "https://www.limon.media/contact")

# 5. FOOTER
st.divider()
st.caption("Limon Media GEO Auditor PRO v1.0 | Stable Build")
