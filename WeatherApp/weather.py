from flask import Flask, render_template, request
import requests
import datetime
import pytz

app = Flask(__name__)

def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

@app.template_filter('datetimefromtimestamp')
def datetimefromtimestamp(value):
    return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        api_key = "4203b1e9e3c8c78bce5439e404363204"
        weather_data = fetch_weather(city, api_key)
        if weather_data:
            temperature = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            temp_min = weather_data['main']['temp_min']
            temp_max = weather_data['main']['temp_max']
            pressure = weather_data['main']['pressure']
            humidity = weather_data['main']['humidity']
            visibility = weather_data.get('visibility', 'N/A') / 1000
            wind_speed = weather_data['wind'].get('speed', 'N/A')
            wind_deg = weather_data['wind'].get('deg', 'N/A')
            clouds = weather_data['clouds'].get('all', 'N/A')
            sunrise = weather_data['sys'].get('sunrise', 'N/A')
            sunset = weather_data['sys'].get('sunset', 'N/A')
            country = weather_data['sys'].get('country', 'N/A')
            coordinates = weather_data['coord']
            timezone_offset = weather_data.get('timezone', 0)
            current_time_utc = datetime.datetime.utcnow()
            current_time_local = current_time_utc + datetime.timedelta(seconds=timezone_offset)
            weather_description = weather_data['weather'][0].get('description', 'N/A')
            weather_icon = weather_data['weather'][0].get('icon', 'N/A')
            
            return render_template('weather.html', city=city, temperature=temperature, feels_like=feels_like,
                                   temp_min=temp_min, temp_max=temp_max, pressure=pressure, humidity=humidity,
                                   visibility=visibility, wind_speed=wind_speed, wind_deg=wind_deg, clouds=clouds,
                                   sunrise=sunrise, sunset=sunset, country=country, coordinates=coordinates,
                                   timezone_offset=timezone_offset, current_time_local=current_time_local,
                                   weather_description=weather_description, weather_icon=weather_icon)
        else:
            error_message = "Failed to fetch weather data. Please try again later."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
