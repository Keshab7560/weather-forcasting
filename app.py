### File: app.py
from flask import Flask, render_template, request
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    forecast_data = []
    if request.method == 'POST':
        city = request.form['city']
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'

        weather_res = requests.get(weather_url)
        forecast_res = requests.get(forecast_url)

        if weather_res.status_code == 200:
            weather_json = weather_res.json()
            weather_data = {
                'city': city,
                'temperature': weather_json['main']['temp'],
                'humidity': weather_json['main']['humidity'],
                'wind_speed': weather_json['wind']['speed'],
                'description': weather_json['weather'][0]['description'].title(),
                'icon': weather_json['weather'][0]['icon']
            }

            forecast_json = forecast_res.json()
            forecast_data = [
                {
                    'datetime': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'icon': item['weather'][0]['icon']
                }
                for item in forecast_json['list'][::8]  # 8 intervals = 24 hrs
            ]
        else:
            weather_data['error'] = "City not found!"

    return render_template('index.html', weather=weather_data, forecast=forecast_data)

@app.route('/auto', methods=['GET'])
def auto_location():
    ip_info = requests.get('https://ipinfo.io/json').json()
    city = ip_info.get('city', 'Delhi')
    return index(city)

if __name__ == '__main__':
    app.run(debug=True)
