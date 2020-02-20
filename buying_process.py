import purchase
import time
import requests
from settings import delay


class Buyingprocess:
    def __init__(self, search_id, profile, option=None):
        self.profile = profile
        self.option = option
        self.search_id = search_id

    def run(self, variant, base_cookies, base_url):
        # TODO add some kind of error handling to keep track of status of process
        # TODO Create something so that the User can know the status of thr buys
        session = requests.session()
        session.cookies = base_cookies
        response = purchase.add_to_cart(session, base_url, variant)
        time.sleep(delay)
        # first part of form
        (response_info, checkout_link, authenticity_token) = purchase.submit_customer_info(session, self.profile,
                                                                                           base_url)
        time.sleep(delay)
        response_ship, session = purchase.get_shipping2(checkout_link, session, response_info.text, authenticity_token)
        time.sleep(delay)
        # payment token
        payment_token = purchase.get_payment_token(self.profile)
        # submitting payment
        purchase.submit_payment2(response_ship, session, checkout_link, self.profile, payment_token)
        print("Done")
