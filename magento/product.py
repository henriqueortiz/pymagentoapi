import requests
import json
from magento.client import Api


class Product(Api):

    def __init__(self):
        self.endpoints = {
            'get_product': '{}/rest/V1/products/{}'.format(self.domain)
        }

    def get_product(self, sku):
        url = self.endpoints['get_product'].format(sku)
        response = requests.request("GET", url, headers=self.headers)
        return json.loads(response.text)
