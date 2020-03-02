import requests
import json
import queue


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


def get_variant(product, options):
    if len(product["variants"]) == 1:
        return product["variants"][0]['id']
    else:
        p_queue = queue.PriorityQueue()
        # Go through each variant for the product
        for variant in product["variants"]:
            closeness = 0
            # Check if the options is found
            for option in product["options"]:
                if option["name"].lowercase() in options:
                    if variant["option%s" % option["position"]] == options[option["name"].lower()]:
                        closeness += 1
            if closeness == options["not_none"]:
                return variant["id"]
            else:
                p_queue.put((-closeness, variant["id"]))
        return p_queue.get()[1]



