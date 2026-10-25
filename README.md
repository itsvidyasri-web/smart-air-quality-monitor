#  Smart Air Quality & Weather Alert System

> Real-time Air Quality, Weather Forecast & Rain Alert Monitoring System for any city.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![API](https://img.shields.io/badge/API-Open--Meteo-green)

### 📖 Overview
This project monitors live environmental data. Users can enter any city (like Nellikuppam, Cuddalore, Chennai) and get instant air pollution and weather updates.

### ✨ Key Features
- **📍 Smart City Search:** Geocoding-based search for any city worldwide
- **🌬️ Live Air Quality:** PM2.5, PM10, CO, NO2, O3 values with status (Good/Moderate/Poor)
- **🌧️ New Feature: Rain Alert System**
    - Live Rain Forecast (mm)
    - Heavy Rain / Light Rain / No Rain Alert
    - Max Temperature Display
- **📈 Interactive Analytics:** Hourly PM2.5 trend graph using Plotly

### 🛠️ How it works?
1.  User enters city name -> `Geocoding API` converts to Latitude/Longitude
2.  Lat/Lon using `Air Quality API` -> Gets Pollution data
3.  Same Lat/Lon using `Weather Forecast API` -> Gets Rain & Temp data
4.  Logic checks `rain_sum` value and triggers Alert

### 💻 Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **APIs:** Open-Meteo (Geocoding, Air-Quality, Forecast)
- **Libraries:** Pandas, Requests, Plotly

### 🚀 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
