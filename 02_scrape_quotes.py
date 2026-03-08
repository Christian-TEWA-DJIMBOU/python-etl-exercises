import requests
from bs4 import BeautifulSoup
import json

quotes = []

for page in range(1, 11):
    url = f"https://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', class_='quote')
    if not divs:
        break

    for div in divs:
        text = div.find('span', class_='text').text.strip().replace('\u201c', '').replace('\u201d', '')
        author = div.find('small', class_='author').text.strip()
        tags = [tag.text for tag in div.find_all('a', class_='tag')]

        quotes.append({
            'quote': text,
            'author': author,
            'tags': tags
        })

with open('output/quotes_data.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print(f"{len(quotes)} quotes scraped and saved to output/quotes_data.json")

authors = {}
for q in quotes:
    authors[q['author']] = authors.get(q['author'], 0) + 1

top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 authors:")
for author, count in top_authors:
    print(f"  {author}: {count} quotes")
