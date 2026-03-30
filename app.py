import streamlit as st
import pandas as pd
import re

# Page configuration
st.set_page_config(
    page_title="UK Emissions Forecast Chatbot",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load aggregated data
@st.cache_data
def load_data():
    df = pd.read_csv("emissions_data.csv")
    return df

df = load_data()

# Load forecast data
@st.cache_data
def load_forecasts():
    transport_forecast = {
        2024: 113255.40, 2025: 113283.09, 2026: 113268.13, 2027: 113276.21,
        2028: 113271.84, 2029: 113274.20, 2030: 113272.93, 2031: 113273.62,
        2032: 113273.24, 2033: 113273.45
    }
    
    co2_forecast = {
        2024: 267398.94, 2025: 266869.89, 2026: 265595.07, 2027: 265902.13,
        2028: 266653.36, 2029: 266378.75, 2030: 264365.38, 2031: 264434.55,
        2032: 264880.18, 2033: 266112.99
    }
    
    transport_prophet = {
        2024: 111254.99, 2025: 111825.00, 2026: 111703.92, 2027: 110890.27,
        2028: 105834.41, 2029: 106404.42, 2030: 106283.33, 2031: 105469.69,
        2032: 100413.83, 2033: 100983.83
    }
    
    co2_prophet = {
        2024: 260977.52, 2025: 248751.25, 2026: 234309.81, 2027: 217651.69,
        2028: 202447.95, 2029: 190221.68, 2030: 175780.24, 2031: 159122.12,
        2032: 143918.37, 2033: 131692.10
    }
    
    return transport_forecast, co2_forecast, transport_prophet, co2_prophet

transport_forecast, co2_forecast, transport_prophet, co2_prophet = load_forecasts()

# Chatbot logic
def get_transport_forecast_data(years_ahead=10):
    years = sorted(list(transport_forecast.keys()))[:years_ahead]
    result = "🚗 Transport Emissions ARIMA Forecast:\n\n"
    for year in years:
        result += f"  {year}: {transport_forecast[year]:,.2f} kt CO2e\n"
    return result

def get_co2_forecast_data(years_ahead=10):
    years = sorted(list(co2_forecast.keys()))[:years_ahead]
    result = "🌍 National CO2 Emissions ARIMA Forecast:\n\n"
    for year in years:
        result += f"  {year}: {co2_forecast[year]:,.2f} kt CO2e\n"
    return result

def get_historical_transport(year):
    row = df[df['Year'] == year]
    if not row.empty:
        value = row['TransportEmissions'].values[0]
        return f"🚗 Transport Emissions in {year}: {value:,.2f} kt CO2e"
    else:
        return f"❌ No data available for year {year}. Available years: 2005-2023"

def get_historical_co2(year):
    row = df[df['Year'] == year]
    if not row.empty:
        value = row['CO2Emissions'].values[0]
        return f"🌍 National CO2 Emissions in {year}: {value:,.2f} kt CO2e"
    else:
        return f"❌ No data available for year {year}. Available years: 2005-2023"

def compare_models_data():
    result = "📊 Model Comparison (ARIMA vs Prophet - Transport Sector):\n\n"
    result += "| Year | ARIMA | Prophet | Difference |\n"
    result += "|------|-------|---------|------------|\n"
    
    for year in sorted(transport_forecast.keys()):
        arima_val = transport_forecast[year]
        prophet_val = transport_prophet[year]
        diff = arima_val - prophet_val
        result += f"| {year} | {arima_val:,.0f} | {prophet_val:,.0f} | {diff:+,.0f} |\n"
    
    return result

def get_model_info():
    return """📊 **UK Emissions Forecast Models**

🔹 **ARIMA Model (Transport Sector)**
   • Order: (1,1,1)
   • Training data: 2005-2023 UK transport emissions
   • Forecast horizon: 2024-2033 (10 years)
   • Use case: Stable trend forecasting

🔹 **Prophet Model (Transport Sector)**
   • Algorithm: Facebook's Prophet
   • Captures trend and seasonality
   • Forecast horizon: 2024-2033
   • Use case: Pattern detection

🔹 **ARIMA Model (National CO2)**
   • Order: (5,1,6) - optimized via grid search
   • Training data: 2005-2023 UK national CO2 emissions
   • Forecast horizon: 2024-2033

🔹 **Prophet Model (National CO2)**
   • Algorithm: Facebook's Prophet
   • Forecast horizon: 2024-2033

📏 **Units:** kt CO2e (kilotons of CO2 equivalent)"""

def parse_question(question):
    question_lower = question.lower()
    
    # Extract year
    year_match = re.search(r'\b(20\d{2})\b', question)
    year = int(year_match.group(1)) if year_match else None
    
    # Comparison
    if any(word in question_lower for word in ['compare', 'comparison', 'vs', 'versus', 'difference']):
        return compare_models_data()
    
    # Model info
    if 'model' in question_lower and any(word in question_lower for word in ['available', 'summary', 'about', 'tell', 'info', 'what']):
        return get_model_info()
    
    # Historical data
    if year and year <= 2023:
        if 'transport' in question_lower:
            return get_historical_transport(year)
        elif any(word in question_lower for word in ['co2', 'carbon', 'national']):
            return get_historical_co2(year)
        else:
            return get_historical_transport(year)
    
    # Future forecast
    if year and year > 2023:
        years_ahead = min(year - 2023, 10)
        if any(word in question_lower for word in ['co2', 'carbon', 'national']):
            return get_co2_forecast_data(years_ahead)
        else:
            return get_transport_forecast_data(years_ahead)
    
    # "next X years"
    next_years_match = re.search(r'next\s+(\d+)\s+years?', question_lower)
    if next_years_match:
        years_ahead = min(int(next_years_match.group(1)), 10)
        if any(word in question_lower for word in ['co2', 'carbon', 'national']):
            return get_co2_forecast_data(years_ahead)
        else:
            return get_transport_forecast_data(years_ahead)
    
    # Keywords
    if any(word in question_lower for word in ['co2', 'carbon', 'national']):
        if any(word in question_lower for word in ['forecast', 'future', 'prediction', 'predict']):
            return get_co2_forecast_data(10)
    elif 'transport' in question_lower:
        if any(word in question_lower for word in ['forecast', 'future', 'prediction', 'predict']):
            return get_transport_forecast_data(10)
    
    return get_model_info()

# Main UI
st.markdown('<h1 class="main-header">🌍 UK Emissions Forecast Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions about UK greenhouse gas emissions and get instant forecasts</p>', unsafe_allow_html=True)

# Example questions
with st.expander("💡 Example Questions"):
    st.markdown("""
    - What will transport emissions be in 2030?
    - Show me the CO2 forecast for the next 5 years
    - What were transport emissions in 2020?
    - Compare ARIMA and Prophet models
    - Tell me about the available models
    - What are national CO2 emissions forecast for 2028?
    """)

# Chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about UK emissions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = parse_question(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar
with st.sidebar:
    st.header("📈 Quick Stats")
    
    latest_year = df['Year'].max()
    latest_transport = df[df['Year'] == latest_year]['TransportEmissions'].values[0]
    latest_co2 = df[df['Year'] == latest_year]['CO2Emissions'].values[0]
    
    st.metric("Latest Year", latest_year)
    st.metric("Transport Emissions", f"{latest_transport:,.0f} kt CO2e")
    st.metric("National CO2", f"{latest_co2:,.0f} kt CO2e")
    
    st.markdown("---")
    
    st.subheader("🔮 2030 Forecasts")
    st.write(f"**Transport:** {transport_forecast[2030]:,.0f} kt")
    st.write(f"**CO2:** {co2_forecast[2030]:,.0f} kt")
    
    st.markdown("---")
    st.caption("Data: UK GHG 2005-2023")
    st.caption("Models: ARIMA & Prophet")
