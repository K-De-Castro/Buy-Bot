
import requests
import json
from bs4 import BeautifulSoup as soup
import random
import control
import time

# TODO add error handling


def generate_cart_link(base_url, variant):
    # generate cart link
    link = base_url + "/cart/" + variant + ":1"
    return link


def add_to_cart(session, base_url, variant):
    # Add the product to cart
    link = base_url + "/cart/add.js?quantity=1&id=" + str(variant)
    response = session.get(link, verify=False)

    # Return the response
    return response


def get_payment_token(checkout_info):
    # POST information to get the payment token
    # link = "https://elb.deposit.shopifycs.com/sessions"
    link = "https://deposit.us.shopifycs.com/sessions"
    payload = {
        "credit_card": {
            "number": checkout_info['card_number'],
            "name": checkout_info['cardholder'],
            "month": checkout_info['exp_m'],
            "year": checkout_info['exp_y'],
            "verification_value": checkout_info['cvv']
        }
    }

    r = requests.post(link, json=payload, verify=False)

    # Extract the payment token
    payment_token = json.loads(r.text)["id"]
    return payment_token


def submit_customer_info(session, checkout_info, base_url):
    # Submit the customer info

    link = base_url + "//checkout.json"
    response = session.get(link, verify=False)

    # getting authenticity_token
    bs = soup(response.text, "html.parser")
    authenticity_token = bs.find("input", {"name": "authenticity_token"})['value']

    # Get the checkout URL
    link = response.url
    checkout_link = link

    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": authenticity_token,
        "previous_step": "contact_information",
        "step": "shipping_method",
        "checkout[email_or_phone]": checkout_info['email'],
        "checkout[buyer_accepts_marketing]": "0",
        "checkout[shipping_address][first_name]": checkout_info['fname'],
        "checkout[shipping_address][last_name]": checkout_info['lname'],
        "checkout[shipping_address][company]": "",
        "checkout[shipping_address][address1]": checkout_info['addy1'],
        "checkout[shipping_address][address2]": checkout_info['addy2'],
        "checkout[shipping_address][city]": checkout_info['city'],
        "checkout[shipping_address][country]": checkout_info['country'],
        "checkout[shipping_address][province]": checkout_info['state'],
        "checkout[shipping_address][zip]": checkout_info['postal_code'],
        "checkout[shipping_address][phone]": checkout_info['phone'],
        "checkout[remember_me]": "0",
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][color_depth]": "24",
        "checkout[client_details][java_enabled]": "false",
        "checkout[client_details][browser_tz]": "360",
        "button": ""
    }
    # POST the data to the checkout URL
    response2 = session.post(link, headers={'User-Agent': 'Mozilla/5.0'}, data=payload, verify=False)
    # Return the response and the checkout link
    return (response2, checkout_link, authenticity_token)


def get_shipping(base_url, session, checkout_info, cookie_jar):
    # Get the shipping rate info from the Shopify site
    link = base_url + "/cart/shipping_rates.json?shipping_address[zip]=" + checkout_info['postal_code'] + "&shipping_address[country]=" + checkout_info['country'] + "&shipping_address[province]=" + checkout_info['state']
    r = session.get(link, cookies=cookie_jar, verify=False)

    # Load the shipping options
    shipping_options = json.loads(r.text)

    # Select the first shipping option
    ship_opt = shipping_options["shipping_rates"][0]["name"].replace(' ', "%20")
    ship_prc = shipping_options["shipping_rates"][0]["price"]

    # Generate the shipping token to submit with checkout
    shipping_option = "shopify-" + ship_opt + "-" + ship_prc

    # Return the shipping option
    return shipping_option


def get_shipping2(shipping_url, session, response_html, authenticity_token):
    print(shipping_url)
    bs = soup(response_html, "html.parser")
    shipping_option = bs.find("input", {"name": "checkout[shipping_rate][id]"})['value']

    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": authenticity_token,
        "button": "",
        "previous_step": "shipping_method",
        "step": "payment_method",
        "checkout[shipping_rate][id]": shipping_option,
    }

    response = session.post(shipping_url, headers={'User-Agent': 'Mozilla/5.0'}, data=payload, verify=False)

    return response, session


def submit_payment2(response, session, checkout_link, checkout_info, payment_token, lock):

    bs = soup(response.text, "html.parser")
    authenticity_token = bs.find("input", {"name": "authenticity_token"})['value']
    payment_gateway = bs.find("input", {"name": "checkout[payment_gateway]"})['value']
    price = bs.find("input", {"name": "checkout[total_price]"})['value']

    if control.can_purchase(float(price)/100, lock):
        payload = {
            "utf8": u"\u2713",
            "_method": "patch",
            "authenticity_token": authenticity_token,
            "previous_step": "payment_method",
            "step": "",
            "s": payment_token,
            "checkout[payment_gateway]": payment_gateway,
            "checkout[credit_card][vault]": "false",
            "checkout[different_billing_address]": "false",
            "checkout[billing_address][first_name]": checkout_info['fname'],
            "checkout[billing_address][last_name]": checkout_info['lname'],
            "checkout[billing_address][company]": '',
            "checkout[billing_address][address1]": checkout_info['addy1'],
            "checkout[billing_address][address2]": checkout_info['addy2'],
            "checkout[billing_address][city]": checkout_info['city'],
            "checkout[billing_address][country]": checkout_info['country'],
            "checkout[billing_address][state]": checkout_info['state'],
            "checkout[billing_address][zip]": checkout_info['postal_code'],
            "checkout[billing_address][phone]": checkout_info['phone'],
            "checkout[total_price]": price,
            "complete": "1",
            "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
            "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
            "checkout[client_details][javascript_enabled]": "1",
            }

        r = session.post(response.url, headers={'User-Agent': 'Mozilla/5.0'}, data=payload, verify=False, allow_redirects=True)
    else:
        print("not enough money")


def debug_submit_payment(response, session, checkout_link, checkout_info, payment_token, lock):
    bs = soup(response.text, "html.parser")
    authenticity_token = bs.find("input", {"name": "authenticity_token"})['value']
    payment_gateway = bs.find("input", {"name": "checkout[payment_gateway]"})['value']
    price = bs.find("input", {"name": "checkout[total_price]"})['value']

    if control.can_purchase(float(price) / 100, lock):
        print(float(price)/100.0)

        payload = {
            "utf8": u"\u2713",
            "_method": "patch",
            "authenticity_token": authenticity_token,
            "previous_step": "payment_method",
            "step": "",
            "s": payment_token,
            "checkout[payment_gateway]": payment_gateway,
            "checkout[credit_card][vault]": "false",
            "checkout[different_billing_address]": "false",
            "checkout[billing_address][first_name]": checkout_info['fname'],
            "checkout[billing_address][last_name]": checkout_info['lname'],
            "checkout[billing_address][company]": '',
            "checkout[billing_address][address1]": checkout_info['addy1'],
            "checkout[billing_address][address2]": checkout_info['addy2'],
            "checkout[billing_address][city]": checkout_info['city'],
            "checkout[billing_address][country]": checkout_info['country'],
            "checkout[billing_address][state]": checkout_info['state'],
            "checkout[billing_address][zip]": checkout_info['postal_code'],
            "checkout[billing_address][phone]": checkout_info['phone'],
            "checkout[total_price]": price,
            "complete": "1",
            "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
            "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
            "checkout[client_details][javascript_enabled]": "1",
        }
    else:
        print("not enough money")

