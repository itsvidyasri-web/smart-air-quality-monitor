
# Tamil Nadu Universal Air Quality and Weather Monitoring System

> Real-time Air Quality, Weather Forecast and Rain Alert System supporting any location worldwide with focus on Tamil Nadu, Karnataka and Telangana.
>
   Live Demo: https://smart-air-quality-monitor-ntz6apcbs4ezsnuefycafm.streamlit.app/
### Overview
This is a real-time environmental monitoring system built with Streamlit. Users can type any city, district or state name and get instant air quality and weather updates. The system uses geocoding to convert location names to coordinates and fetches live data from Open-Meteo APIs.

### Key Features
- **Universal Location Search:** Type any location - supports all 38 districts of Tamil Nadu, Karnataka, Telangana and worldwide
- **Smart Search with Auto-Correction:** If multiple locations found, system shows selection for accurate results
- **Live Air Quality Monitoring:** PM2.5 and PM10 with AQI categorization (Good / Satisfactory / Moderate / Poor)
- **Weather and Rain Alert System:** 
    - Daily rainfall prediction (mm)
    - Temperature monitoring (Current, Max, Min)
    - Accurate alerts: Heavy Rain (>7.5mm), Light Rain (>0.2mm), No Rain
- **Interactive Analytics:** Dual graph visualization - 24-hour PM2.5 and PM10 trend analysis using Plotly
- **Professional Navigation:** Dashboard and About sections with clean UI

### App Screenshot
![App Screenshot](screenshot.png)
<img width="1600" height="900" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/fe88c112-9771-411c-8c01-17ba96b4d0d2" />
<img width="1600" height="900" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/b5cb164b-7af2-47a2-ba80-1f6709ba0a34" />
<img width="1600" height="900" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/2d2ee076-c706-4f1f-aad9-5eda0ff2cb47" />

### How It Works

1.  User types location name (e.g., Chennai, Bengaluru, Hyderabad)
2.  Geocoding API converts location to Latitude and Longitude
3.  Air Quality API fetches PM2.5 and PM10 data using coordinates
4.  Weather Forecast API fetches rainfall and temperature data
5.  System displays metrics, alerts and trend graphs

### Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **APIs:** Open-Meteo (Geocoding, Air Quality, Weather Forecast)
- **Libraries:** Pandas, Requests, Plotly

### How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
