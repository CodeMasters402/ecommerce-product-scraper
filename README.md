# E-commerce Product Scraper

A small, clean demo scraper built with `requests` + `BeautifulSoup`. It scrapes product name, price, availability and detail-page URL from [Books to Scrape](https://books.toscrape.com/) — a practice site made for learning web scraping — follows the catalogue pagination, and saves everything to `products.csv`.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python scraper.py
```

## Sample output

The full run collects 1,000 products from 50 pages. The first rows of `products.csv` look like this:

```csv
title,price,availability,url
A Light in the Attic,£51.77,In stock,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
Tipping the Velvet,£53.74,In stock,https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html
Soumission,£50.10,In stock,https://books.toscrape.com/catalogue/soumission_998/index.html
```

A 20-row sample is committed as `sample_products.csv`. The full `products.csv` is ignored by git (see `.gitignore`).

## How it works

1. `fetch_page` downloads a catalogue page with a plain, honest User-Agent.
2. `parse_products` reads each `article.product_pod`: the title from the link's `title` attribute (the visible text is truncated), the price, the availability text, and the detail-page URL.
3. `next_page_url` follows the "next" link until the last page.
4. Everything is written to `products.csv` with a short summary printed at the end.

Built by [CodeMasters](https://codemasters402.github.io/) — custom web scrapers, clean Excel/CSV data, fixed quote before starting.
