import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Weather Dashboard", page_icon="https://cdn-icons-png.flaticon.com/512/552/552448.png", layout="wide")

st.title("🌦️Weather ForecasterModel Z")

city = st.text_input("Enter a city name:", "Chicago")

def get_weather_emoji(code):
    if code in [0, 1]:
        return "☀️"
    elif code in [2]:
        return "⛅"
    elif code in [3]:
        return "☁️"
    elif code in [45, 48]:
        return "🌫️"
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "❄️"
    elif code in [95, 96, 99]:
        return "⛈️"
    else:
        return "🌡️"

geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
geo_res = requests.get(geo_url).json()

if "results" in geo_res:
    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]
    country = geo_res["results"][0].get("country", "")

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
    weather_res = requests.get(weather_url).json()

    daily_data = weather_res["daily"]

    st.markdown("---")
    st.subheader(f"7-Day Forecast for {city.title()}, {country}")

    formatted_dates = []

    cols = st.columns(7)
    for i in range(7):
        raw_date = daily_data["time"][i]
        date_obj = datetime.strptime(raw_date, "%Y-%m-%d")
        clean_date = date_obj.strftime("%a %d")
        formatted_dates.append(clean_date)

        max_temp = daily_data["temperature_2m_max"][i]
        min_temp = daily_data["temperature_2m_min"][i]
        w_code = daily_data["weathercode"][i]
        emoji = get_weather_emoji(w_code)

        with cols[i]:
            st.metric(label=f"{clean_date} {emoji}", value=f"{max_temp}°C")
            st.caption(f"Min: {min_temp}°C")

    st.markdown("---")
    st.subheader("Temperature Trend (Next 7 Days)")

    chart_data = pd.DataFrame({
        "Max Temperature": daily_data["temperature_2m_max"],
        "Min Temperature": daily_data["temperature_2m_min"]
    }, index=formatted_dates)

    st.line_chart(chart_data)

else:
    st.error("⚠️ City not found. Please check your spelling and try again.")