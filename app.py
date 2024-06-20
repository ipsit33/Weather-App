from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('index.html', weather_data=weather_data)

def get_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'location': {
                'name': data['location']['name'],
                'region': data['location']['region'],
                'country': data['location']['country'],
                'localtime': data['location']['localtime']
            },
            'current': {
                'temp_c': data['current']['temp_c'],
                'temp_f': data['current']['temp_f'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'wind_kph': data['current']['wind_kph'],
                'wind_dir': data['current']['wind_dir'],
                'pressure_mb': data['current']['pressure_mb'],
                'humidity': data['current']['humidity'],
                'feelslike_c': data['current']['feelslike_c'],
                'uv': data['current']['uv'],
                'gust_kph': data['current']['gust_kph'],
                'air_quality': data['current']['air_quality']
            }
        }
        return weather
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
