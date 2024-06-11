import streamlit as st
import requests
import pandas as pd

# OpenWeatherMap API 키를 여기에 입력하세요.
API_KEY = '344c9bcbfcf9ce399a6104a00569ba47'

def get_coordinates(city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

def get_weather(lat, lon, forecast=False):
    if forecast:
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr'
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr'
    
    response = requests.get(url)
    return response.json()

def parse_current_weather(data):
    main = data['main']
    weather = data['weather'][0]
    wind = data['wind']
    sys = data['sys']
    return {
        "Temperature (°C)": main['temp'],
        "Feels Like (°C)": main['feels_like'],
        "Min Temperature (°C)": main['temp_min'],
        "Max Temperature (°C)": main['temp_max'],
        "Pressure (hPa)": main['pressure'],
        "Humidity (%)": main['humidity'],
        "Weather": weather['description'],
        "Wind Speed (m/s)": wind['speed'],
        "Sunrise": pd.to_datetime(sys['sunrise'], unit='s'),
        "Sunset": pd.to_datetime(sys['sunset'], unit='s')
    }

def parse_forecast_weather(data):
    forecast_list = []
    for item in data['list']:
        main = item['main']
        weather = item['weather'][0]
        wind = item['wind']
        forecast_list.append({
            "Date and Time": item['dt_txt'],
            "Temperature (°C)": main['temp'],
            "Feels Like (°C)": main['feels_like'],
            "Min Temperature (°C)": main['temp_min'],
            "Max Temperature (°C)": main['temp_max'],
            "Pressure (hPa)": main['pressure'],
            "Humidity (%)": main['humidity'],
            "Weather": weather['description'],
            "Wind Speed (m/s)": wind['speed']
        })
    return forecast_list

def main():
    st.title('날씨 예보 앱')
    
    city = st.text_input('도시 이름을 입력하세요:')
    
    if st.button('현재 날씨 조회'):
        lat, lon = get_coordinates(city)
        if lat and lon:
            weather = get_weather(lat, lon)
            if weather:
                current_weather = parse_current_weather(weather)
                st.write(f"{city}의 현재 날씨 정보:")
                st.table(pd.DataFrame([current_weather]))  # 표로 출력
            else:
                st.write("날씨 정보를 가져올 수 없습니다.")
        else:
            st.write("도시를 찾을 수 없습니다.")
    
    if st.button('미래 날씨 예보 조회'):
        lat, lon = get_coordinates(city)
        if lat and lon:
            forecast = get_weather(lat, lon, forecast=True)
            if forecast:
                forecast_weather = parse_forecast_weather(forecast)
                st.write(f"{city}의 날씨 예보 정보:")
                st.table(pd.DataFrame(forecast_weather))  # 표로 출력
            else:
                st.write("날씨 예보 정보를 가져올 수 없습니다.")
        else:
            st.write("도시를 찾을 수 없습니다.")

if __name__ == '__main__':
    main()
