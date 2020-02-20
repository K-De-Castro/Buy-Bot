import requests
import json

# TODO add error handling

def get_product(session, base_url):
    url = base_url + "/products.json"
    r = session.get(url, verify=False)
    response = json.loads(r.text)
    return response['products']


def keywords_search(products, keywords):
    for product in products:
        keys = 0
        for keyword in keywords:
            if keyword.upper() in product["title"].upper():
                keys += 1
            if keys == len(keywords):
                return product
    return None


def get_variant(product, option):
    if len(product["variants"]) == 1:
        return product["variants"][0]['id']
    else:
        # Go through each variant for the product
        for variant in product["variants"]:
            # Check if the option is found
            if option in variant["title"]:
                variant = str(variant["id"])
                return variant


