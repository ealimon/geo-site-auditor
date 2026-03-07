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
    .stButton>button:hover {
        background-color: #e6c200;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CORE ENGINE: UNIVERSAL STABILITY
def run_geo_audit(url, niche):
    try:
        # Connects to your Streamlit Secrets
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Using the base 'gemini-1.5-flash' name to prevent 404/Connection errors
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"You are a Senior GEO Strategist. Perform an audit for: {url} in the {niche} niche. "
            "\n\nFormat your response as follows:"
            "\n1. **AI Sentiment Analysis** (How LLMs perceive this brand)"
            "\n2. **Information Density** (Technical scannability for AI agents)"
            "\n3. **Citation Potential** (Likelihood of being sourced in AI answers)"
            "\n4. **Top 3 Action Items** to immediately improve AI search visibility."
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return str(e)

# 3. SIDEBAR: BETA BRANDING
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.write("**GEO Auditor PRO** (Beta Access)")
    st.caption("Specialized AI tools for the generative search era.")
    
    st.divider()
    
    st.markdown("#### **Beta Support**")
    st.write("Found a bug or have a feature request?")
    st.link_button("📩 Send Feedback", "mailto:info@limon.media")
    
    st.divider()
    
    st.markdown("#### **Need an Expert?**")
    st.write("Full-service GEO implementation for high-growth brands.")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")
    
    st.divider()
    st.caption("© 2026 Limon Media")

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
        with st.spinner("Analyzing digital footprint..."):
            result = run_geo_audit(target_url, niche)
            
            # Friendly Error Handling for "Beta" users
            if "429" in result:
                st.error("🍋 **System Busy.** Google's free tier is temporarily full. Please wait 60 seconds and try again.")
            elif "404" in result or "not found" in result.lower():
                st.error("🍋 **Connection Error.** Please refresh the page to reconnect to the AI engine.")
            elif "API_KEY_INVALID" in result:
                st.error("🍋 **Key Error.** Please check your Streamlit Secrets configuration.")
            else:
                st.success("Audit Complete!")
                st.markdown(result)
                st.divider()
                st.balloons()
                st.markdown("### 🍋 Want to dominate AI Search?")
                st.link_button("Contact Limon Media", "https://www.limon.media/contact")

# 5. FOOTER
st.divider()
st.caption("Limon Media GEO Auditor PRO v1.0 | Stable Beta Build")
