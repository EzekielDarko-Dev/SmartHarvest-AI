# 🌾 SmartHarvest AI

AI-powered Streamlit app helping Ghanaian smallholder farmers with planting advice, market intelligence, and crop emergency diagnosis — built with Gemma 4.

**Team:** Agrificial Intelligence (Ezekiel Owusu, Simon Essel)
**Hackathon:** Build with Gemma Hackathon 2026

## The Problem
Ghanaian smallholder farmers lose income at almost every stage — planting at the wrong time, missing early signs of crop disease, having no access to agricultural experts, and selling at low prices to middlemen due to poor market information.

## Our Solution
Three features, all powered by Gemma 4 via the Google GenAI SDK:
- 🌱 **Planting Advisor** — seasonal viability, timeline, risk score, and cost estimates by crop/region/month
- 📈 **Market Intelligence** — pricing trends, middlemen advice, cheap preservation methods
- 🚨 **Crop Emergency Advisor** — symptom-based diagnosis and treatment advice

## Tech Stack
Python · Streamlit · Google GenAI SDK · Gemma 4 (`gemma-4-26b-a4b-it`) · python-dotenv

## Setup
1. Clone this repo
2. `pip install -r requirements.txt`
3. Create a `.env` file with `GEMINI_API_KEY=your_key_here`
4. `streamlit run app.py`
