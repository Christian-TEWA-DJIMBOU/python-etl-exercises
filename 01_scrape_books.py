import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/page-1.html"
books = []

for page in range(1, 6):
    page_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text.strip().replace('£', '')
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating_text = article.find('p', class_='star-rating')['class'][1]
        rating = rating_map.get(rating_text, 0)
        availability = article.find('p', class_='instock availability').text.strip()

        books.append({
            'title': title,
            'price': float(price),
            'rating': rating,
            'availability': availability
        })

with open('output/books_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating', 'availability'])
    writer.writeheader()
    writer.writerows(books)

print(f"{len(books)} books scraped and saved to output/books_data.csv")

top_rated = [b for b in books if b['rating'] >= 4]
avg_price = sum(b['price'] for b in books) / len(books)

print(f"Top rated books (4+): {len(top_rated)}")
print(f"Average price: £{avg_price:.2f}")
