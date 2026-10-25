
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Smart Air Quality Monitor",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Smart Air Quality Monitoring")
st.write(
    "Live air-quality information and forecast "
    "using the Open-Meteo API."
)

cities = {
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Bengaluru": (12.9716, 77.5946),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777)
}

city = st.selectbox("Choose your city", list(cities.keys()))
latitude, longitude = cities[city]

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "pm2_5,pm10,us_aqi",
    "hourly": "pm2_5,pm10,us_aqi",
    "forecast_days": 1,
    "timezone": "auto"
}

if st.button("Get Air Quality Data"):
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})

        st.subheader(f"Current Air Quality: {city}")

        aqi = current.get("us_aqi")
        pm25 = current.get("pm2_5")
        pm10 = current.get("pm10")

        col1, col2, col3 = st.columns(3)
        col1.metric("US AQI", aqi if aqi is not None else "N/A")
        col2.metric("PM2.5 (µg/m³)", pm25 if pm25 is not None else "N/A")
        col3.metric("PM10 (µg/m³)", pm10 if pm10 is not None else "N/A")

        if aqi is not None:
            if aqi <= 50:
                st.success("Good air quality")
            elif aqi <= 100:
                st.info("Moderate air quality")
            elif aqi <= 150:
                st.warning("Unhealthy for sensitive groups")
            elif aqi <= 200:
                st.warning("Unhealthy air quality")
            else:
                st.error("Very unhealthy or hazardous air quality")

        hourly = data.get("hourly", {})
        df = pd.DataFrame({
            "Time": hourly.get("time", []),
            "PM2.5": hourly.get("pm2_5", []),
            "PM10": hourly.get("pm10", []),
            "US AQI": hourly.get("us_aqi", [])
        })

        if not df.empty:
            st.subheader("Air Quality Trend and Forecast")
            df["Time"] = pd.to_datetime(df["Time"])
            st.line_chart(df.set_index("Time")[["PM2.5", "PM10"]])
            st.line_chart(df.set_index("Time")[["US AQI"]])

            st.download_button(
                "Download Data as CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name=f"{city.lower()}_air_quality.csv",
                mime="text/csv"
            )

    except requests.RequestException:
        st.error("Unable to connect to the air-quality API. Please try again.")
    except (ValueError, KeyError):
        st.error("The API returned data in an unexpected format.")

st.caption(
    "Data source: Open-Meteo Air Quality API. "
    "Values are model-based estimates, not direct sensor readings. "
    "Forecasts are not guaranteed."
)
