import json
import requests
from django.shortcuts import redirect
from django.contrib import messages

from .configuration import number_products
from .constants import INFO1, INFO2, INFO3, INFO4, URL_GENERAL, NUTRIMENTS,\
    FAT, SATURATED_FAT, SUGAR, SALT

# number_products = 20

# URL_GENERAL = 'https://fr.openfoodfacts.org/cgi/search.pl'

# the different category keys to insert them into the database
# INFO1 = "product_name_fr"
# INFO2 = "image_front_thumb_url"
# INFO3 = "nutrition_grade_fr"
# INFO4 = "url"
# NUTRIMENTS = "nutriments"
# FAT = "fat"
# SATURATED_FAT = "saturated-fat"
# SUGAR = "sugars"
# SALT = "salt"


class DataApi:
    """the request to the API which contains the parameters"""
    def __init__(self, product):
        self.url = URL_GENERAL

        self.payload_products_generic_name = {
            'search_terms': product,
            'page_size': number_products,
            'json': 'true',
        }

    def get_nutriscore_food_choose(self):
        response = requests.get(self.url,
                                params=self.payload_products_generic_name)
        if 'json' in response.headers.get('Content-Type'):
            try:
                data = response.json()["products"][0]["nutrition_grade_fr"]
            except (IndexError, KeyError):
                data = "e"
            return data

    def get_categories_name_food(self):
        """Obtain the food category chosen by the user"""
        response = requests.get(self.url, params=self.payload_products_generic_name)
        if 'json' in response.headers.get('Content-Type'):
            try:
                data = response.json()["products"][0]["categories"]
                return data
            except (IndexError, KeyError):
                data = "cassoulet"
                return data
        else:
            print('response content is not in json format.')
            data = 'spam'
        return data

    def get_data_products_category(self, category_product):
        """get the data of the chosen category"""
        payload_substitutes = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category_product,
            'page_size': number_products,
            'json': 'true',
        }
        response = requests.get(self.url, params=payload_substitutes).json()
        data = response["products"]
        return data

    def select_key_test(self, key1=INFO1, key2=INFO2, key3=INFO3, key4=INFO4,
                        key5=NUTRIMENTS, key6=FAT, key7=SATURATED_FAT,
                        key8=SUGAR, key9=SALT):
        """The different keys are sorted and placed in lists"""
        list_general = []
        categories = self.get_categories_name_food()
        category = self.get_category_selected(categories)

        data = self.get_data_products_category(category)
        for item in data:
            product_list = [item.get(key1), item.get(key2), item.get(key3),
                            item.get(key4), item.get(key5).get(key6),
                            item.get(key5).get(key7), item.get(key5).get(key8),
                            item.get(key5).get(key9)]
            if '' not in product_list and None not in product_list:
                list_general.append(product_list)
        return list_general

    def get_category_selected(self, categories):
        """Sort the name of the food categories to obtain valid data"""
        categories_list = categories.split(",")
        category = categories_list[0]
        return category


