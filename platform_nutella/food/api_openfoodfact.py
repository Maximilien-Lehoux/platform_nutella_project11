import requests
import json

API_TO_PRODUCT_FIELDS = {
    'product_name_fr': 'name',
    'url': 'url',
    'nutrition_grade_fr': 'nutriscore',
    'category': 'category'
    }

CATEGORIES = ["volailles",
              "cereales-et-pommes-de-terre",
              "aliments-d-origine-vegetale",
              "aliments-a-base-de-fruits-et-de-legumes",
              "plats-prepares"]

category_example = ["volailles"]

NUMBER_PRODUCTS = 100

payload_products_generic_name = {
                    'search_terms': 'nutella',
                    'page_size': NUMBER_PRODUCTS,
                    'json': 'true',
                    }

payload_substitutes = {
                    'action': 'process',
                    'tagtype_0': 'categories',
                    'tag_contains_0': 'contains',
                    'tag_0': 'Pâte à tartiner aux noisettes et au cacao',
                    'page_size': NUMBER_PRODUCTS,
                    'json': 'true',
                    }

# https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=P%C3%A2te_%C3%A0_tartiner_aux_noisettes_et_au_cacao


# payload_products = {'action': 'process',
                    # 'tagtype_0': 'categories',
                    # 'tag_contains_0': 'contains',
                    # 'search_terms': 'nutella',
                    # 'tagtype_1': 'nutrition_grade',
                    # 'tag_contains_1': 'contains',
                    # 'tag_1': 'a',
                    # 'fields': ','.join(API_TO_PRODUCT_FIELDS.keys()),
                    # 'page_size': NUMBER_PRODUCTS,
                    # 'page': 5,
                    # 'json': 'true',
                    # }


URL_GENERAL = 'https://fr.openfoodfacts.org/cgi/search.pl'


class DataApi:
    """the request to the API which contains the parameters"""
    def __init__(self, url):
        self.url = url

    def get_generic_name_food(self):
        response = requests.get(self.url, params=payload_products_generic_name)
        if 'json' in response.headers.get('Content-Type'):
            data = response.json()["products"][0]["generic_name"]
        else:
            print('response content is not in json format.')
            data = 'spam'
        return data

    def get_data_products_category(self):
        response = requests.get(self.url, params=payload_substitutes).json()
        data = response["products"]
        with open("file_json.json", "w") as file:
            json.dump(data, file, sort_keys=True, indent=4)
        return data

    def select_key_test(self, key1, key2, key3, key4):
        """The different keys are sorted and placed in lists"""
        list_general = []
        data = self.get_data_products_category()
        for item in data:
            product_list = [item.get(key1), item.get(key2), item.get(key3),
                            item.get(key4)]
            if '' not in product_list and None not in product_list:
                list_general.append(product_list)
        return list_general

# 'product_name_fr', 'generic_name_fr', 'url', 'image_front_thumb_url', 'nutrition_grade_fr'


example_data_api = DataApi(URL_GENERAL)
data_nutella = example_data_api.get_generic_name_food()
print(data_nutella)


data_products_category = example_data_api.select_key_test('product_name_fr', 'image_front_thumb_url', 'nutrition_grade_fr', 'url')
print(data_products_category)


# 'image_front_thumb_url'
# 'selected_images': {'front': {'display': {'fr'

