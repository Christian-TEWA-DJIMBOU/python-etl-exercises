import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://books.toscrape.com/catalogue/"
all_books = []

page = 1
while True:
    url = f"{base_url}page-{page}.html"
    response = requests.get(url)

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')

    if not articles:
        break

    for article in articles:
        title = article.h3.a['title']
        price = float(article.find('p', class_='price_color').text.strip().replace('£', ''))
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(article.find('p', class_='star-rating')['class'][1], 0)

        detail_url = base_url + article.h3.a['href']
        detail_response = requests.get(detail_url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        table = detail_soup.find('table', class_='table-striped')
        rows = table.find_all('tr')
        upc = rows[0].td.text
        stock_text = rows[5].td.text
        stock = int(''.join(filter(str.isdigit, stock_text)))
        category = detail_soup.find('ul', class_='breadcrumb').find_all('li')[2].a.text.strip()

        all_books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'upc': upc,
            'stock': stock,
            'category': category
        })

    print(f"Page {page} scraped ({len(articles)} books)")
    page += 1

    if page > 5:
        break

with open('output/books_detailed.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'price', 'rating', 'upc', 'stock', 'category'])
    writer.writeheader()
    writer.writerows(all_books)

print(f"\n{len(all_books)} books saved to output/books_detailed.csv")

categories = {}
for book in all_books:
    cat = book['category']
    if cat not in categories:
        categories[cat] = {'count': 0, 'total_price': 0}
    categories[cat]['count'] += 1
    categories[cat]['total_price'] += book['price']

print("\nStats by category:")
for cat, stats in sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True):
    avg = stats['total_price'] / stats['count']
    print(f"  {cat}: {stats['count']} books, avg price: £{avg:.2f}")
