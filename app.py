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

# 2. CORE LOGIC
def get_best_model():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for preferred in ['gemini-2.0-flash', 'gemini-1.5-flash']:
            for m in models:
                if preferred in m: return m
        return models[0]
    except Exception:
        return "gemini-1.5-flash"

# 3. SIDEBAR
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.divider()
    st.markdown("### 🛠️ More Tools")
    st.info("**Coming Soon:** AI Content Sentiment Scorer")
    st.divider()
    st.markdown("#### **Need an Expert?**")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")

# 4. MAIN INTERFACE
st.title("GEO Auditor PRO")
col1, col2 = st.columns(2)
with col1:
    target_url = st.text_input("Website URL", placeholder="https://yourbrand.com")
with col2:
    niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate")

if st.button("🚀 Run AI GEO Audit"):
    if not target_url or not niche:
        st.warning("Please enter both a URL and a Niche.")
    else:
        try:
            model_name = get_best_model()
            model = genai.GenerativeModel(model_name)
            with st.spinner("Analyzing..."):
                prompt = f"Perform a GEO audit for {target_url} in the {niche} niche. Provide AI Sentiment, Information Density, and 3 Action Items."
                response = model.generate_content(prompt)
                st.success("Audit Complete!")
                st.markdown(response.text)
                st.divider()
                st.markdown("### 🍋 Want to dominate AI Search?")
                st.link_button("Contact Limon Media", "https://www.limon.media/contact")
        except Exception as e:
            st.error(f"Error: {str(e)}")
