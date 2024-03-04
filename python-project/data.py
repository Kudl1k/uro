import requests
import json


response_API = requests.get('https://dummyjson.com/products?limit=100')
print(response_API.status_code)
products = json.loads(response_API.text)['products']