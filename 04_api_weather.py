import requests
import csv
from datetime import datetime

cities = [
    {'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'Lyon', 'lat': 45.7640, 'lon': 4.8357},
    {'name': 'Marseille', 'lat': 43.2965, 'lon': 5.3698},
    {'name': 'Toulouse', 'lat': 43.6047, 'lon': 1.4442},
    {'name': 'Bordeaux', 'lat': 44.8378, 'lon': -0.5792},
    {'name': 'Lille', 'lat': 50.6292, 'lon': 3.0573},
    {'name': 'Nantes', 'lat': 47.2184, 'lon': -1.5536},
    {'name': 'Strasbourg', 'lat': 48.5734, 'lon': 7.7521},
    {'name': 'Nice', 'lat': 43.7102, 'lon': 7.2620},
    {'name': 'Rennes', 'lat': 48.1173, 'lon': -1.6778},
]

weather_data = []

for city in cities:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching {city['name']}: {response.status_code}")
        continue

    data = response.json()
    current = data['current']

    weather_data.append({
        'city': city['name'],
        'temperature': current['temperature_2m'],
        'wind_speed': current['wind_speed_10m'],
        'humidity': current['relative_humidity_2m'],
        'weather_code': current['weather_code'],
        'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    print(f"  {city['name']}: {current['temperature_2m']}°C, wind: {current['wind_speed_10m']} km/h")

with open('output/weather_france.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['city', 'temperature', 'wind_speed', 'humidity', 'weather_code', 'fetched_at'])
    writer.writeheader()
    writer.writerows(weather_data)

print(f"\n{len(weather_data)} cities saved to output/weather_france.csv")

hottest = max(weather_data, key=lambda x: x['temperature'])
coldest = min(weather_data, key=lambda x: x['temperature'])
avg_temp = sum(d['temperature'] for d in weather_data) / len(weather_data)

print(f"\nHottest: {hottest['city']} ({hottest['temperature']}°C)")
print(f"Coldest: {coldest['city']} ({coldest['temperature']}°C)")
print(f"Average: {avg_temp:.1f}°C")
