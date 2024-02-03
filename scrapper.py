# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Function to scrape product information from Amazon
def scrape_amazon_product(url):
    try:
        # Define user-agent headers to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
        }

        # Send a GET request to the Amazon URL
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_name_element = soup.find('span', class_='a-size-large product-title-word-break')

            if product_name_element:
                # Extract and return the product name
                product_name = product_name_element.get_text().strip()[:50]
                price_element = soup.find('span', class_='a-price-whole')
                if price_element:
                    price = price_element.get_text().strip()
                    return product_name, price

    except Exception as e:
        # In case of an exception, return None and the error message
        return None, str(e)

# Function to scrape product information from Snapdeal
def scrape_snapdeal_product(url):
    try:
        # Send an HTTP GET request to the Snapdeal URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('h1', {'class': 'pdp-e-i-head'}).text.strip()
        product_price = soup.find('span', {'class': 'payBlkBig'}).text.strip()
        # Return product name and price (limited to 50 characters for the name)
        return product_name[:50], product_price
    except Exception as e:
        # In case of an exception, return None and the error message
        return None, str(e)

# Input URLs for Amazon and Snapdeal products
amazon_url = input("Enter Amazon Product URL: ")
snapdeal_url = input("Enter Snapdeal Product URL: ")

# Scrape product information from Amazon and Snapdeal
amazon_product_name, amazon_product_price = scrape_amazon_product(amazon_url)
snapdeal_product_name, snapdeal_product_price = scrape_snapdeal_product(snapdeal_url)

# Compare the prices from both websites
if amazon_product_price and snapdeal_product_price and snapdeal_product_price != "'NoneType' object has no attribute 'text'":
    amazon_price = float(amazon_product_price.replace(',', ''))
    snapdeal_price = float(snapdeal_product_price.replace(',', ''))

    # Determine the lowest price and the corresponding website
    min_price = min(amazon_price, snapdeal_price)
    if min_price == amazon_price:
        lowest_price_website = "Amazon"
    else:
        lowest_price_website = "Snapdeal"
else:
    lowest_price_website = "NA"

# Create a table to display the product information
table_data = [
    ['Website', 'Product Name', 'Product Price'],
    ['Amazon', amazon_product_name, amazon_product_price],
    ['Snapdeal', snapdeal_product_name, snapdeal_product_price],
    ['Comparison', '', f'Lowest Price: {lowest_price_website}']
]

# Print the table using tabulate
print(tabulate(table_data, headers='firstrow',
showindex='always',
 tablefmt='grid'))