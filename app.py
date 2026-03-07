import streamlit as st
import google.generativeai as genai
import time

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

# 2. CORE LOGIC: STABLE MODEL SELECTOR
def get_best_model():
    """Uses 1.5 Flash for the highest reliability on Free Tier quotas."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        return "gemini-1.5-flash"
    except Exception:
        return "gemini-1.5-flash"

# 3. SIDEBAR: THE MARKETPLACE
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.write("Testing the future of AI Search Visibility.")
    
    st.divider()
    
    st.markdown("### 🛠️ More Tools")
    st.info("**Coming Soon:** AI Content Sentiment Scorer")
    st.write("🧪 *Internal Beta:* Local Maps LLM Optimizer")
    
    st.divider()
    
    st.markdown("#### **Need an Expert?**")
    st.write("Full-service GEO implementation for high-growth brands.")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")
    
    st.divider()
    st.caption("© 2026 Limon Media | info@limon.media")

# 4. MAIN INTERFACE
st.title("GEO Auditor PRO")
st.markdown("Analyze how **AI Search Engines** perceive your brand in seconds.")

col1, col2 = st.columns(2)
with col1:
    target_url = st.text_input("Website URL", placeholder="https://yourbrand.com")
with col2:
    niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate")

st.divider()

# 5. EXECUTION WITH ERROR HANDLING
if st.button("🚀 Run AI GEO Audit"):
    if not target_url or not niche:
        st.warning("Please enter both a URL and a Niche.")
    else:
        try:
            model_name = get_best_model()
            model = genai.GenerativeModel(model_name)
            
            with st.spinner("Analyzing digital footprint..."):
                prompt = (
                    f"You are a Senior GEO Strategist. Perform an audit for: {target_url} in the {niche} niche. "
                    "\n\nFormat your response as follows:"
                    "\n1. **AI Sentiment Analysis** (How LLMs see you)"
                    "\n2. **Information Density** (Is your site easy for AI to read?)"
                    "\n3. **Citation Potential** (Will AI source you?)"
                    "\n4. **Top 3 Action Items** to improve visibility."
                )
                response = model.generate_content(prompt)
                
                st.success("Audit Complete!")
                st.markdown(response.text)
                
                st.divider()
                st.balloons()
                st.markdown("### 🍋 Want to dominate AI Search?")
                st.link_button("Contact Limon Media", "https://www.limon.media/contact")
                
        except Exception as e:
            # Friendly handling for Quota/429 errors
            if "429" in str(e) or "quota" in str(e).lower():
                st.error("🍋 **System is a bit squeezed!** Our free AI quota is temporarily full. Please wait 60 seconds and try again.")
            else:
                st.error(f"Note: {str(e)}")

# 6. FOOTER
st.divider()
st.caption("Limon Media GEO Auditor PRO v1.0 | Stable Build")
