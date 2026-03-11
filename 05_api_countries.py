import requests
import csv

response = requests.get("https://restcountries.com/v3.1/region/europe")
data = response.json()

countries = []

for country in data:
    name = country.get('name', {}).get('common', 'N/A')
    capital = country.get('capital', ['N/A'])[0] if country.get('capital') else 'N/A'
    population = country.get('population', 0)
    area = country.get('area', 0)
    languages = ', '.join(country.get('languages', {}).values()) if country.get('languages') else 'N/A'
    currencies_data = country.get('currencies', {})
    currency = list(currencies_data.values())[0]['name'] if currencies_data else 'N/A'
    subregion = country.get('subregion', 'N/A')

    density = round(population / area, 2) if area > 0 else 0

    countries.append({
        'name': name,
        'capital': capital,
        'population': population,
        'area_km2': area,
        'density': density,
        'languages': languages,
        'currency': currency,
        'subregion': subregion
    })

countries.sort(key=lambda x: x['population'], reverse=True)

with open('output/european_countries.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'capital', 'population', 'area_km2', 'density', 'languages', 'currency', 'subregion'])
    writer.writeheader()
    writer.writerows(countries)

print(f"{len(countries)} European countries saved to output/european_countries.csv")

top5 = countries[:5]
print("\nTop 5 by population:")
for c in top5:
    print(f"  {c['name']}: {c['population']:,} ({c['capital']})")

avg_density = sum(c['density'] for c in countries) / len(countries)
densest = max(countries, key=lambda x: x['density'])
print(f"\nAverage density: {avg_density:.1f} people/km²")
print(f"Most dense: {densest['name']} ({densest['density']} people/km²)")

subregions = {}
for c in countries:
    sr = c['subregion']
    if sr not in subregions:
        subregions[sr] = 0
    subregions[sr] += c['population']

print("\nPopulation by subregion:")
for sr, pop in sorted(subregions.items(), key=lambda x: x[1], reverse=True):
    print(f"  {sr}: {pop:,}")
