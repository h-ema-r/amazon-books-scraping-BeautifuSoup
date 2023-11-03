from bs4 import BeautifulSoup
import requests
import csv

# Change the user-agent value based on your web browser
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

csv_headers = ['Rank', 'Title', 'Author', 'Price']

with open('amazon_books_multi.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

page_number = 1  # Start with the first page

while True:
    url = f"https://www.amazon.com/Best-Sellers-Books/zgbs/books?_encoding=UTF8&pg={page_number}"

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    books = soup.find_all(id="gridItemRoot")

    if not books:
        break  # If no books are found on the page, exit the loop

    for book in books:
        rank = book.find('span', class_='zg-bdg-text').text[1:]

        children = book.find('div', class_='zg-grid-general-faceout').div
        title = children.contents[1].text
        author = children.contents[2].text
        price = children.contents[-1].text

        with open('amazon_books_multi.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([rank, title, author, price])

    page_number += 1  # Move to the next page
