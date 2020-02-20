import search
import time
import requests
import random
import threading
import concurrent.futures
from settings import delay


class Searchprocess:
    def __init__(self, url, item_words, option=None):
        self.base_url = url
        self.id = random.seed
        self.keywords = [item_words]
        self.option = option
        self.session = requests.session()
        self.buys = []

    def add_buy(self, buy):
        self.buys.append(buy)

    def remove_keywords(self, index):
        self.keywords.pop(index)

    def product_search(self, products, keywords):
        return search.keywords_search(products, keywords)

    def run(self):
        catalog = self.base_url + "/collections/all"
        while len(self.keywords) != 0:
            products = search.get_product(self.session, catalog)
            # threads to search for different product at the same time
            # as soon as one 1 is found run the buying processes for them in that they're own thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = {executor.submit(self.product_search, products, self.keywords[i]): [self.keywords[i], i] for i in range(len(self.keywords))}
                for product_info in concurrent.futures.as_completed(results):
                    search_info = results[product_info]
                    product = product_info.result()
                    if product:
                        print(product)
                        self.keywords.pop(search_info[1])
                        # TODO add some way to incorporate options i.e size(shoes, shirts, etc), color, others
                        variant = search.get_variant(product, None)
                        # Will be leaving statuses up to something else that I'll make later/ error handling systems
                        with concurrent.futures.ThreadPoolExecutor() as e:
                            for j in range(len(self.buys)):
                                e.submit(self.buys[j].run, variant, self.session.cookies, self.base_url)