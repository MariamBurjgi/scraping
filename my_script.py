import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import schedule
import time

conn = sqlite3.connect('product_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price TEXT,
        description TEXT
    )
''')
#I defined list of products-url
product_urls = [
    "https://www.hecht-garten.ch/do-it-garten/reinigungsgeraete/kehrmaschine/hecht-8101-bs-kehrmaschine/a-11908/",
    
]

def scrape_product_info(url):
    # here is http get request
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        #product information
        product_name_element = soup.find("h1", class_="product_name")
        product_name = product_name_element.text.strip() if product_name_element else "Product name not found"

        product_price_element = soup.find("span", class_="price")
        product_price = product_price_element.text.strip() if product_price_element else "Price not found"

        # load the previous product information from json
        try:
            with open("product_info.json", "r") as json_file:
                previous_product_data = json.load(json_file)
        except FileNotFoundError:
            previous_product_data = {}

        #changes checking
        if previous_product_data.get("price") != product_price:
            print(f"Price has changed from {previous_product_data.get('price', 'N/A')} to {product_price}")

        # here are updated and saved the product information to json
        product_data = {
            "name": product_name,
            "price": product_price,
            "deleted": False,  
           
        }

        return product_data

    else:
        print(f"The page does not exist (404 Not Found) for URL: {url}")
        return None

def scrape_and_update_all_products():
    all_products = []

    for url in product_urls:
        product_data = scrape_product_info(url)
        if product_data:
            all_products.append(product_data)

    # i saved information for all products to json
    with open("all_products_info.json", "w") as json_file:
        json.dump(all_products, json_file, indent=4)

    print("All product information updated and saved to all_products_info.json")

# this is schedule script to run every 24 hours
schedule.every(24).hours.do(scrape_and_update_all_products)

while True:
    schedule.run_pending()
    time.sleep(1)
