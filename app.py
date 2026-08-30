import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()
api_key = os.getenv("AQ.Ab8RN6J68094yU-FCkk2ciIFLDQnWAZjJY0kZi2phgnZ7RF4yA")

# Set up the Google GenAI Client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY not found. Please check your .env file!")
    st.stop()

# Define the System Instruction with market, agronomic, and emergency skills
SYSTEM_INSTRUCTION = (
    "You are an expert Ghanaian Agronomist, Agricultural Extension Officer, and Market Intelligence Agent. "
    "Your goal is to help smallholder farmers maximize crop yields and profits while mitigating risks. "
    "You understand regional rainy seasons, local market pricing dynamics (e.g., in Takoradi, Accra, Kumasi), "
    "and common challenges like spoilage and middle-men pricing pressure. Keep advice simple, highly specific to Ghana, "
    "and deeply practical. Always suggest cheap, accessible local preservation methods. "
    "Format outputs using clear markdown headings and clean bullet points."
)

# App Title & UI Configuration
st.set_page_config(page_title="SmartHarvest AI", page_icon="🌾", layout="centered")
st.title("🌾 SmartHarvest AI")
st.write("Your personal AI agricultural companion, risk advisor, and market intelligence assistant.")

# Create the three tabs
tab1, tab2, tab3 = st.tabs(["📅 On-Farm Assistant", "📈 Market Intelligence", "🚨 Crop Emergency"])

# --- TAB 1: ON-FARM ASSISTANT ---
with tab1:
    st.header("Crop Planting & Care Scheduler")
    
    col1, col2 = st.columns(2)
    with col1:
        crop_tab1 = st.selectbox("Select Crop", ["Maize", "Cassava", "Tomato", "Cocoa"], key="crop1")
        region_tab1 = st.selectbox(
            "Region",
            ["Western", "Ashanti", "Greater Accra", "Northern", "Volta", "Eastern"],
            key="region1"
        )
    with col2:
        month_tab1 = st.selectbox("Planned Planting Month", [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ], key="month1")
        
    if st.button("Generate Planting Plan", type="primary"):
        with st.spinner("Analyzing soil seasons, climate data, and calculating risk..."):
            prompt = (
                f"Analyze the crop '{crop_tab1}' in the '{region_tab1}' region of Ghana, assuming I plan to start planting in '{month_tab1}'.\n\n"
                "Please structure your response exactly with these sections:\n"
                "1. **Seasonal Viability**: Is this a good time to start? Consider the seasonal rainfall patterns in this selected region before recommending.\n"
                "2. **Estimated Timeline**: Best time to start and expected harvest time.\n"
                "3. **Risk Level Score**: Provide a clear risk rating using exactly one of these labels: '🟢 Low Risk', '🟡 Medium Risk', or '🔴 High Risk', followed by a brief explanation of why.\n"
                "4. **Financial Estimates**: Based on standard local rates in Ghana for this crop, give an approximate breakdown of:\n"
                "   - Approximate seed cost (per acre)\n"
                "   - Fertilizer/input cost (per acre)\n"
                "   - Expected yield (per acre)\n"
                "   - Expected profit/revenue (per acre in GHS)\n"
                "5. **Post-Planting Care**: Essential checklist of what to do right after planting."
            )
            try:
                # Utilizing the latest Gemma 4 26B Mixture-of-Experts model via Google GenAI SDK
                response = client.models.generate_content(
                    model="gemma-4-26b-a4b-it", # Latest Gemma 4 model
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION
                    )
                )
                st.success("✅ Analysis Complete!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- TAB 2: MARKET INTELLIGENCE ---
with tab2:
    st.header("Beyond the Farm Gate (Market Advisor)")
    col1, col2, col3 = st.columns(3)
    with col1:
        crop_tab2 = st.selectbox("Select Crop", ["Tomato", "Cassava", "Maize", "Cocoa"], key="crop2")
    with col2:
        location_tab2 = st.selectbox("Your Nearest Market", ["Takoradi", "Accra", "Kumasi", "Tamale"])
    with col3:
        month_tab2 = st.selectbox("Estimated Harvest Month", [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ], key="month2")
        
    if st.button("Get Market Report", type="primary"):
        with st.spinner("Calculating market trends..."):
            prompt = (
                f"Analyze the crop '{crop_tab2}' with an estimated harvest in '{month_tab2}' near '{location_tab2}'. "
                "Act as my market intelligence agent and tell me:\n"
                "1) What is the general pricing trend for this crop in this region during this month?\n"
                "2) How should I handle middle-men buyers specifically in Ghana?\n"
                "3) Give me 2 extremely cheap, local ways to preserve this crop from spoiling while I wait for a fair price."
            )
            try:
                response = client.models.generate_content(
                    model="gemma-4-26b-a4b-it",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION
                    )
                )
                st.success("✅ Market Report Generated!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- TAB 3: CROP EMERGENCY ADVISOR ---
with tab3:
    st.header("🚨 Crop Emergency Advisor")
    st.write("Is something wrong with your crops? Describe the issues, spots, or pests you are seeing, and get immediate diagnostic help.")
    
    col1, col2 = st.columns(2)
    with col1:
        emergency_crop = st.selectbox("Affected Crop", ["Maize", "Cassava", "Tomato", "Cocoa"], key="emergency_crop")
    with col2:
        emergency_region = st.selectbox(
            "Your Region",
            ["Western", "Ashanti", "Greater Accra", "Northern", "Volta", "Eastern"],
            key="emergency_region"
        )
        
    user_description = st.text_area(
        "Describe what you are seeing (e.g., 'My maize leaves are turning yellow and curling')",
        placeholder="Type the symptoms of your crop disease here..."
    )
    
    if st.button("Diagnose Issue", type="primary"):
        if not user_description.strip():
            st.warning("Please describe the symptoms before diagnosing!")
        else:
            with st.spinner("Analyzing symptoms and looking up remedies..."):
                prompt = (
                    f"My '{emergency_crop}' in the '{emergency_region}' region is showing these symptoms: '{user_description}'.\n\n"
                    "Act as an immediate agricultural emergency diagnostic tool and provide:\n"
                    "1. **Possible Causes**: What disease or pest does this sound like? Give 1 or 2 likely suspects.\n"
                    "2. **Immediate Action**: What should I do *today* to stop it from spreading?\n"
                    "3. **Prevention Tips**: How do I prevent this from happening next season using cheap, accessible methods?"
                )
                try:
                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    st.success("🏥 Emergency Diagnosis Complete!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
      
