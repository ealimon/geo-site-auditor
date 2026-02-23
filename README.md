🍋 Limon AI: GEO Site Auditor
An AI-powered SEO tool designed to audit websites for Generative Engine Optimization (GEO). This tool analyzes how well a site is positioned to be cited by AI search engines like Google Gemini, Perplexity, and ChatGPT.

🚀 Features
AI-Powered Analysis: Uses Google Gemini 1.5 Flash to identify content gaps.

Credit System: Integrated with Lemon Squeezy to provide 10 audits per license key.

Atomic Answers: Generates LLM-optimized summaries for better AI visibility.

🛠️ Setup & Installation
1. Environment Variables (Secrets)
To run this app, you must add the following keys to your Streamlit Cloud Secrets or a local .env file:

GOOGLE_API_KEY: Your API key from Google AI Studio.

LEMON_API_KEY: Your API key from the Lemon Squeezy Settings dashboard.

2. Local Deployment
Bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
💳 Payment Integration
This app is configured to work with Lemon Squeezy.

Users purchase a "10-Audit Pack" on your storefront.

The app validates the license key via the /licenses/validate endpoint.

Each successful audit triggers an /licenses/activate call to decrement one credit.

⚠️ Troubleshooting
KeyError: Ensure your Secrets are correctly named in the Streamlit Dashboard.

Invalid License: Check that the product in Lemon Squeezy has License Keys enabled and the Activation Limit is set to 10.

A Quick "Clean House" Tip
Before you push this to GitHub, make sure you delete any old Gumroad-related files or test scripts. Keeping your repository clean makes it much easier for Streamlit to deploy without errors.
