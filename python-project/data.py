import requests
import json
import random
import string

response_API = requests.get('https://dummyjson.com/products?limit=100')
print(response_API.status_code)
unformated_products = json.loads(response_API.text)['products']



products = []
for product in unformated_products:
    # Generate random placement
    placement = str(random.randint(1, 5)) + random.choice(string.ascii_uppercase[:4])
    formatted_product = {
        "id": product["id"],
        "title": product["title"],
        "description": product["description"],
        "price": product["price"],
        "stock": product["stock"],
        "brand": product["brand"],
        "category": product["category"],
        "thumbnail": product["thumbnail"],
        "images": product["images"],
        "placement": placement
    }
    products.append(formatted_product)