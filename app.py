import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Universal Air Quality Monitor", layout="wide")

# --- CSS - PRO THEME ---
st.markdown("""
<style>
    .stTextInput input { font-size: 18px !important; }
    h1, h2, h3 { color: #111827; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_coordinates(city_name: str):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=5&language=en"
        res = requests.get(url, timeout=10).json()
        if res.get("results"):
            return res["results"] # Return top 5 matches
        return []
    except Exception:
        return []

@st.cache_data(ttl=600)
def get_env_data(lat: float, lon: float):
    try:
        air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10&timezone=auto"
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=rain_sum,temperature_2m_max,temperature_2m_min,weathercode&current_weather=true&timezone=auto"
        air = requests.get(air_url, timeout=10).json()
        weather = requests.get(weather_url, timeout=10).json()
        return air, weather
    except Exception:
        return None, None

def get_aqi_category(pm25):
    if pm25 <= 30: return "Good", "success"
    elif pm25 <= 60: return "Satisfactory", "info"
    elif pm25 <= 90: return "Moderate", "warning"
    else: return "Poor", "error"

# --- SIDEBAR ---
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["Dashboard", "About"])
    st.divider()
    st.caption("Supports: Tamil Nadu, Karnataka, Telangana and Any Location Worldwide")

# --- MAIN ---
if page == "Dashboard":
    st.title("Universal Air Quality and Weather Monitoring System")
    st.write("Type any city, district, or state. Example: Cuddalore, Bengaluru, Hyderabad, Mumbai, Delhi, Nellikuppam")

    # TYPING SEARCH
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        city_input = st.text_input("Enter Location", placeholder="Type location name here... e.g. Chennai, Mysore, Warangal", label_visibility="collapsed")
    with col_btn:
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if search_btn and city_input:
        results = get_coordinates(city_input)
        
        if not results:
            st.error(f"No location found for '{city_input}'. Please check spelling and try again.")
            st.stop()
        
        # If multiple results, let user select correct one
        if len(results) > 1:
            options = [f"{r['name']}, {r.get('admin1','')}, {r.get('country','')} (Lat:{r['latitude']:.2f})" for r in results]
            selected_option = st.selectbox("Multiple locations found. Select correct location:", options)
            selected_index = options.index(selected_option)
            location = results[selected_index]
        else:
            location = results[0]

        lat = location['latitude']
        lon = location['longitude']
        display_name = f"{location['name']}, {location.get('admin1','')}, {location.get('country','')}"

        with st.spinner(f"Fetching data for {display_name}..."):
            air_data, weather_data = get_env_data(lat, lon)

        if not air_data or not weather_data:
            st.error("Data fetch failed.")
            st.stop()

        pm25 = air_data['hourly']['pm2_5'][0]
        pm10 = air_data['hourly']['pm10'][0]
        rain = weather_data['daily']['rain_sum'][0]
        max_temp = weather_data['daily']['temperature_2m_max'][0]
        min_temp = weather_data['daily']['temperature_2m_min'][0]
        curr_temp = weather_data.get('current_weather', {}).get('temperature', 0)
        
        status, alert_type = get_aqi_category(pm25)

        st.divider()
        st.subheader(f"Live Report: {display_name}")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("PM2.5", f"{pm25} µg/m³", status)
        c2.metric("PM10", f"{pm10} µg/m³")
        c3.metric("Rainfall Today", f"{rain} mm")
        c4.metric("Temperature", f"{curr_temp} °C", f"{min_temp}° to {max_temp}°")

        st.divider()
        # ALERTS
        a1, a2 = st.columns(2)
        with a1:
            st.subheader("Weather Alert")
            if rain > 7.5:
                st.error(f"Heavy Rain Alert: {rain} mm rainfall expected in {display_name}.")
            elif rain > 0.2:
                st.warning(f"Light Rain Alert: {rain} mm rainfall expected in {display_name}.")
            else:
                st.success(f"No Rain: Clear weather in {display_name}.")

        with a2:
            st.subheader("Air Quality Alert")
            if status == "Poor":
                st.error(f"Air Quality is Poor in {display_name}. Limit outdoor activity.")
            elif status == "Moderate":
                st.warning(f"Air Quality is Moderate in {display_name}.")
            else:
                st.success(f"Air Quality is {status} in {display_name}.")

        # TWO GRAPHS
        st.divider()
        st.subheader("24-Hour Trend Analysis")
        df = pd.DataFrame(air_data['hourly']).head(24)
        g1, g2 = st.columns(2)
        with g1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=df.index, y=df['pm2_5'], mode='lines+markers', line=dict(color='#2563eb')))
            fig1.update_layout(title="PM2.5 Trend", xaxis_title="Hour", yaxis_title="µg/m³", template="plotly_white", height=380)
            st.plotly_chart(fig1, use_container_width=True)
        with g2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['pm10'], mode='lines+markers', line=dict(color='#7c3aed')))
            fig2.update_layout(title="PM10 Trend", xaxis_title="Hour", yaxis_title="µg/m³", template="plotly_white", height=380)
            st.plotly_chart(fig2, use_container_width=True)

    elif search_btn and not city_input:
        st.warning("Please type a location name first.")

else:
    st.title("About")
    st.markdown("""
    This system supports universal location search.
    
    **You can search:**
    - All 38 Districts of Tamil Nadu
    - Karnataka: Bengaluru, Mysore, Mangalore, Hubli etc.
    - Telangana: Hyderabad, Warangal, Karimnagar etc.
    - Any city worldwide
    
    **How it works:**
    1. Type location name -> Geocoding API finds latitude/longitude
    2. Fetches Air Quality and Weather from Open-Meteo
    3. Displays alerts and graphs
    """)
