import settings
import search
import requests
import purchase
from search_process import Searchprocess
from buying_process import Buyingprocess

#initializing

base_url = settings.base_url  # url of shopify store homepage
catalog = settings.catalog  # url for all items of shopify store
checkout_info = settings.check_info  # user info for checkout

process = Searchprocess(base_url, settings.keywords)
for i in range(2):
    process.add_buy(Buyingprocess(process.id, settings.check_info))
process.run()
