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
        stock TEXT,
        description TEXT
        image_url TEXT,
        supplier_id TEXT,
        categories TEXT,
        last_updated DATETIME
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
        
        stock_element = soup.find("span", class_="stock_info")
        product_stock = stock_element.text.strip() if stock_element else "Stock information not found"

        description_element = soup.find("div", class_="product_description")
        product_description = description_element.text.strip() if description_element else "Description not found"

        image_element = soup.find("img", class_="product_image")
        image_url = image_element["src"] if image_element else "Image not found"

        supplier_id_element = soup.find("span", class_="supplier_id")
        supplier_id = supplier_id_element.text.strip() if supplier_id_element else "Supplier product ID not found"

        categories_elements = soup.find_all("span", class_="category")
        categories = [category.text.strip() for category in categories_elements]
        
        cursor.execute('''
            SELECT id, price
            FROM products
            WHERE name = ?
            ORDER BY last_updated DESC
            LIMIT 1
        ''', (product_name,))
        result = cursor.fetchone()
        product_id = result[0] if result else None
        old_price = result[1] if result else None
        
        if old_price is not None and old_price != product_price:
            print(f"Price has changed for '{product_name}' from {old_price} to {product_price}")
        
        cursor.execute('''
            INSERT INTO products (name, price, stock, description, image_url, supplier_id, categories, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (product_name, product_price, product_stock, product_description, image_url, supplier_id, ", ".join(categories)))

        conn.commit()
        
    else:
        print(f"The page does not exist (404 Not Found) for URL: {url}")
       
    def scrape_and_update_all_products():
        for url in product_urls:
            scrape_product_info(url)

# Schedule the script to run every 24 hours
#schedule.every(24).hours.do(scrape_and_update_all_products)

while True:
    schedule.run_pending()
    time.sleep(1)
    
    product_urls = [
        "https://www.hecht-garten.ch/do-it-garten/reinigungsgeraete/kehrmaschine/hecht-8101-bs-kehrmaschine/a-11908/",
        "https://example.com/another-product",
        "https://example.com/yet-another-product",
    # Adding more
]
    for url in product_urls:
        scrape_product_info(url)
    for url in product_urls:
        scrape_product_info(url)


    """ cursor.execute('''
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
"""