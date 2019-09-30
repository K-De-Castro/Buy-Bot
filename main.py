import settings
import search
import requests
import purchase
import tkinter

#initializing
base_url = settings.base_url
catalog = settings.catalog
checkout_info = settings.check_info

session = requests.session()
products = search.get_product(session, catalog)
product = search.keywords_search(products, settings.keywords)
variant = search.get_variant(product, None)
print(variant)
print(isinstance(variant, str))

response = purchase.add_to_cart(session, base_url, variant)

cookies = response.cookies

payment_token = purchase.get_payment_token(checkout_info)

(response_info, checkout_link, authenticity_token) = purchase.submit_customer_info(session, settings.check_info, cookies, base_url)

# ship = purchase.get_shipping(base_url, session, checkout_info, cookies)
response_ship = purchase.get_shipping2(checkout_link, session, cookies, response_info.text, authenticity_token)

# Get the payment gateway ID
# link = checkout_link + "?step=payment_method"

# submitting payment
purchase.submit_payment(response_ship, base_url, checkout_link, checkout_info)

# r = session.get(payment_url, cookies=cookies, verify=False)
#
# bs = soup(r.text, "html.parser")
# gateway = bs.find("input", {"name": "checkout[payment_gateway]"})['value']
# print(gateway)
#
# # Submit the payment
# # link = checkout_link
#
# payload = {
#     "utf8": u"\u2713",
#     "_method": "patch",
#     "authenticity_token": authenticity_token,
#     "previous_step": "payment_method",
#     "step": "",
#     "s": payment_token,
#     "checkout[payment_gateway]": gateway,
#     "checkout[credit_card][vault]": "false",
#     "checkout[different_billing_address]": "true",
#     "checkout[billing_address][first_name]": checkout_info['fname'],
#     "checkout[billing_address][last_name]": checkout_info['lname'],
#     "checkout[billing_address][address1]": checkout_info['addy1'],
#     "checkout[billing_address][address2]": checkout_info['addy2'],
#     "checkout[billing_address][city]": checkout_info['city'],
#     "checkout[billing_address][country]": checkout_info['country'],
#     "checkout[billing_address][state]": checkout_info['state'],
#     "checkout[billing_address][zip]": checkout_info['postal_code'],
#     "checkout[remember_me]": False,
#     "checkout[remember_me]": 0,
#     "complete": "1",
#     "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
#     "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
#     "checkout[client_details][javascript_enabled]": "1",
#     "checkout[client_details][color_depth]": "24",
#     "checkout[client_details][browser_tz]": "360",
#     "g-recaptcha-response": "",
#     "button": ""
#     }
#
# r = session.post(checkout_link, headers={'User-Agent': 'Mozilla/5.0'}, cookies=cookies, data=payload, verify=False)


