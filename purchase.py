from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup as soup
import random
import time

def generate_cart_link(base_url, variant):
    #generate cart link
    link = base_url + "/cart/" + variant + ":1"
    return link

def get_payment_token(checkout_info):
    # POST information to get the payment token
    link = "https://elb.deposit.shopifycs.com/sessions"

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


def submit_customer_info(session, checkout_info, cookie_jar, base_url):
    # Submit the customer info

    link = base_url + "//checkout.json"
    response = session.get(link,  cookies=cookie_jar, verify=False)

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
        "checkout[client_details][javascript_enabled]": "1",
        "button": ""
    }
    # POST the data to the checkout URL
    response = session.post(link, headers={'User-Agent': 'Mozilla/5.0'}, cookies=cookie_jar, data=payload, verify=False)

    # Return the response and the checkout link
    return (response, checkout_link, authenticity_token)


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


def get_shipping2(shipping_url, session, cookies_jar, response_html, authenticity_token):

    bs = soup(response_html, "html.parser")
    shipping_option = bs.find("input", {"name": "checkout[shipping_rate][id]"})['value']
    payload = {
        "utf8": u"\u2713",
        "_method": "patch",
        "authenticity_token": authenticity_token,
        "previous_step": "shipping_method",
        "step": "payment_method",
        "checkout[shipping_rate][id]": shipping_option,
        "checkout[client_details][browser_width]": "1710",
        "checkout[client_details][browser_height]": "1289",
        "checkout[client_details][color_depth]": "24",
        "checkout[client_details][javascript_enabled]": "1",
        "checkout[client_details][browser_tz]": "360",
        "button": ""
    }

    response = session.post(shipping_url, headers={'User-Agent': 'Mozilla/5.0'}, cookies=cookies_jar, data=payload, verify=False)

    return response


def add_to_cart(session, base_url,  variant):
    # Add the product to cart
    link = base_url + "/cart/add.js?quantity=1&id=" + str(variant)
    response = session.get(link, verify=False)

    # Return the response
    return response


def submit_payment(response, base_url, checkout_link, checkout_info):
    chrome_path = r"C:\Users\Kevin\Desktop\Programming stuff\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    link = checkout_link + "?step=payment_method"

    # converting cookies from session to driver
    cookies_dict = response.cookies.get_dict()
    driver.get(base_url)
    for cookie in cookies_dict:
        driver.add_cookie({'name': cookie, 'value': cookies_dict[cookie]})

    # opening payment page
    driver.get(link)

    # adding cc number
    driver.switch_to.frame(1)

    cc_number = driver.find_element_by_xpath('//*[@id="number"]')

    cc_number.send_keys(checkout_info['card_number'])

    # adding cc name
    driver.switch_to.default_content()
    driver.switch_to.frame(2)

    cc_name = driver.find_element_by_xpath('//*[@id="name"]')

    cc_name.send_keys(checkout_info['cardholder'])

    # adding cc experation date
    driver.switch_to.default_content()
    driver.switch_to.frame(3)

    cc_name = driver.find_element_by_xpath('//*[@id="expiry"]')

    cc_name.send_keys(checkout_info['exp_m'] + checkout_info['exp_y'])

    # adding cc experation ccv
    driver.switch_to.default_content()
    driver.switch_to.frame(4)

    cc_name = driver.find_element_by_xpath('//*[@id="verification_value"]')

    cc_name.send_keys(checkout_info['cvv'])

    # adding billing address
    driver.switch_to.default_content()

    different_baddress = driver.find_element_by_xpath('//*[@id="checkout_different_billing_address_true"]')
    different_baddress.click()

    # first name
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_first_name"]').send_keys(checkout_info['fname'])

    # last name
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_last_name"]').send_keys(checkout_info['lname'])

    # address1
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_address1"]').send_keys(checkout_info['addy1'])

    # address2
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_address2"]').send_keys(checkout_info['addy2'])

    # city
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_city"]').send_keys(checkout_info['city'])

    # country
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_country"]/option[1]').click()

    # state
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_province"]/option[8]').click()

    # zipcode
    driver.find_element_by_xpath('//*[@id="checkout_billing_address_zip"]').send_keys(checkout_info['postal_code'])

    # submit
    driver.find_element_by_xpath('//*[@id="continue_button"]').click()

    while "thank_you" not in driver.current_url:
        time.sleep(2)