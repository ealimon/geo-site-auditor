import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="GEO Auditor PRO | Limon Media", 
    page_icon="🍋", 
    layout="wide"
)

# Custom CSS to match the Limon Media aesthetic
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

# 2. CORE LOGIC: MODEL SELECTOR
def get_best_model():
    """Dynamically finds the best available Gemini Flash model in the user's project."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prioritize 2026/2025 versions
        for preferred in ['gemini-2.0-flash', 'gemini-1.5-flash']:
            for m in models:
                if preferred in m: return m
        return models[0]
    except Exception:
        return "gemini-1.5-flash"

# 3. SIDEBAR: THE MARKETPLACE & BRANDING
with st.sidebar:
    st.title("🍋 Limon Labs")
    st.write("Welcome to the GEO Beta. We're building the future of AI Search Visibility.")
    
    st.divider()
    
    # FUTURE PRODUCT SHELF (Market Testing Area)
    st.markdown("### 🛠️ More Tools")
    st.info("**Next Release:** AI Content Sentiment Scorer")
    st.write("🧪 *Internal Beta:* Local Maps LLM Optimizer")
    
    st.divider()
    
    # THE AGENCY UPSELL
    st.markdown("#### **Need an Expert?**")
    st.write("We provide full-service GEO implementation for high-growth brands.")
    st.link_button("📅 Book a Strategy Call", "https://www.limon.media/contact")
    
    st.divider()
    st.caption("© 2026 Limon Media | info@limon.media")

# 4. MAIN INTERFACE
st.title("GEO Auditor PRO")
st.markdown("""
    Analyze how **Generative Search Engines** (like Perplexity, SearchGPT, and Gemini) 
    perceive your brand.
""")

# Input Fields
col1, col2 = st.columns(2)
with col1:
    target_url = st.text_input("Website URL", placeholder="https://yourbrand.com")
with col2:
    niche = st.text_input("Business Niche", placeholder="e.g., Luxury Real Estate in Palm Springs")

st.divider()

# 5. EXECUTION LOGIC
if st.button("🚀 Run AI GEO Audit"):
    if not target_url or not niche:
        st.warning("Please enter both a URL and a Niche to run the audit.")
    else:
        try:
            model_name = get_best_model()
            model = genai.GenerativeModel(model_name)
            
            with st.spinner(f"AI is crawling {target_url} for GEO signals..."):
                # Professional Prompt Engineering for high-value output
                prompt = (
                    f"You are a Senior GEO (Generative Engine Optimization) Strategist. "
                    f"Perform a comprehensive audit for the website: {target_url} within the {niche} niche. "
                    "\n\nProvide the analysis in the following format:"
                    "\n1. **AI Sentiment Analysis**: How do LLMs perceive this brand's authority?"
                    "\n2. **Information Density**: Is the content structured for easy AI extraction?"
                    "\n3. **Citation Potential**: How likely is this site to be cited as a primary source?"
                    "\n4. **Top 3 Action Items**: Specific technical or content changes to improve AI rankings."
                )
                
                response = model.generate_content(prompt)
                
                # Render Results
                st.success(f"Audit Complete for {target_url}")
                st.markdown(response.text)
                
                # Final Call to Action
                st.divider()
                st.balloons()
                st.markdown("### 🍋 Want to dominate
