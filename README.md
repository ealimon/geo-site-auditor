# 🍋 Limon AI: GEO Site Auditor

An AI-powered tool designed to audit websites for **Generative Engine Optimization (GEO)**. This application analyzes how effectively a website's content can be cited and surfaced by AI search engines like Google Gemini, Perplexity, and SearchGPT.

## 🚀 Features
- **AI Audit Engine:** Powered by Google Gemini 1.5 Flash for deep content analysis.
- **GEO Readiness Score:** Provides a 1-100 visibility metric.
- **Credit System:** Integrated with **Lemon Squeezy** to provide a 10-audit limit per license key.
- **Actionable Insights:** Identifies specific content gaps to improve AI search ranking.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- A [Google AI Studio](https://aistudio.google.com/) API Key
- A [Lemon Squeezy](https://www.lemonsqueezy.com/) API Key

### 2. Configuration (Secrets)
To keep your API keys safe, this app uses Streamlit's secrets management. **Do not hard-code your keys into the script.** Add the following to your **Streamlit Cloud Secrets** or a local `.streamlit/secrets.toml` file:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
LEMON_API_KEY = "your_lemon_squeezy_api_key_here"
