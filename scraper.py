"""
E-commerce product scraper (demo).

Scrapes product name, price, availability and detail-page URL from
https://books.toscrape.com/ — a practice site made for learning web
scraping. It follows the catalogue pagination and saves everything to
products.csv.

Run:
    python scraper.py
"""

import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")
OUTPUT_FILE = "products.csv"

# A plain, honest User-Agent so the server can see this is a scraper.
HEADERS = {"User-Agent": "CodeMasters-demo-scraper/1.0"}


def fetch_page(url):
    """Download one page and return a parsed BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_products(soup, page_url):
    """Extract the product rows from one catalogue page."""
    products = []
    for article in soup.select("article.product_pod"):
        # Title lives in the link's title attribute; the visible text is
        # truncated, so always use the attribute.
        link = article.select_one("h3 a")
        title = link["title"].strip()
        detail_url = urljoin(page_url, link["href"])
        price = article.select_one("p.price_color").get_text(strip=True)
        # Availability text contains whitespace/newlines; strip it down.
        availability = article.select_one("p.instock.availability").get_text(strip=True)
        products.append(
            {
                "title": title,
                "price": price,
                "availability": availability,
                "url": detail_url,
            }
        )
    return products


def next_page_url(soup, page_url):
    """Return the URL of the next catalogue page, or None on the last page."""
    next_link = soup.select_one("li.next a")
    if next_link is None:
        return None
    return urljoin(page_url, next_link["href"])


def main():
    products = []
    url = START_URL
    pages = 0

    while url:
        soup = fetch_page(url)
        products.extend(parse_products(soup, url))
        pages += 1
        print(f"Page {pages}: {len(products)} products so far...")
        url = next_page_url(soup, url)
        # Be polite: a short pause between requests.
        if url:
            time.sleep(0.2)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "price", "availability", "url"]
        )
        writer.writeheader()
        writer.writerows(products)

    print(f"\nDone: {len(products)} products from {pages} pages.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
