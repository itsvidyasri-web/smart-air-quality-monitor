import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Smart Air Quality Monitor", page_icon="🌿", layout="wide")

# --- FUNCTIONS (Ithu than professional) ---
def get_coordinates(city_name):
    """City name vaangi lat/lon tharum"""
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        res = requests.get(url).json()
        if res.get('results'):
            return res['results'][0]['latitude'], res['results'][0]['longitude'], res['results'][0]['name']
        return None, None, None
    except:
        return None, None, None

def get_air_and_weather(lat, lon):
    """Air quality + Weather + Rain data edukuthu"""
    air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10&timezone=auto"
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=rain_sum,weathercode,temperature_2m_max&timezone=auto"
    
    air_data = requests.get(air_url).json()
    weather_data = requests.get(weather_url).json()
    return air_data, weather_data

# --- UI ---
st.title("🌿 Smart Air Quality Monitor")
st.markdown("**Live Air Quality, Weather & Rain Alert System**")

city = st.selectbox("Oor ah select pannu daa:", ["Chennai", "Cuddalore", "Coimbatore", "Madurai", "Bengaluru", "Delhi", "Nellikuppam"])

if st.button("Check Pannu"):
    lat, lon, name = get_coordinates(city)
    
    if lat:
        air, weather = get_air_and_weather(lat, lon)
        
        # ALERT SYSTEM - Ithu than nee ketta Rain alert!
        rain_today = weather['daily']['rain_sum'][0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("PM2.5", f"{air['hourly']['pm2_5'][0]} µg/m³")
        col2.metric("Rain Today", f"{rain_today} mm")
        col3.metric("Max Temp", f"{weather['daily']['temperature_2m_max'][0]} °C")

        # Professional Alert
        if rain_today > 7.5:
            st.error(f"🚨 HEAVY RAIN ALERT in {name}: Innaiku {rain_today}mm mazhai! Velila porathu safe illa daa!", icon="⛈️")
        elif rain_today > 0.2:
            st.warning(f"🌧️ Rainy Alert: {name} la {rain_today}mm light rain irukku!", icon="🌧️")
        else:
            st.success(f"☀️ No Rain in {name}: Climate sema super ah irukku!", icon="✅")
        
        # Graph
        df = pd.DataFrame(air['hourly'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['pm2_5'], name="PM2.5 Trend"))
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Oor kedaikala daa, vera oor try pannu!")
