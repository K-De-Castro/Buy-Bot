# Global settings
base_url = "https://geeksnfreeks.myshopify.com"  # Don't add a / at the end
catalog = "https://geeksnfreeks.myshopify.com/collections/all"

# Search settings
keywords = ["legend", "ink", "backpack"]  # Seperate keywords with a comma
size = "11"

# If a size is sold out, a random size will be chosen instead, as a backup plan
random_size = True

# To avoid a Shopify soft-ban, a delay of 7.5 seconds is recommended if
# starting a task much earlier than release time (minutes before release)
# Otherwise, a 1 second or less delay will be ideal
search_delay = 7.5

# Checkout settings
check_info = {
    'email': '',
    'fname': 'Bill',
    'lname': 'Nye',
    'addy1': "",
    'addy2': "",  # Can be left blank
    'city': "",
    'state': "",
    'country': "United States",
    'postal_code': "",
    'phone': "4169671111",
    'card_number': "4242 4242 4242 4242",  # No spaces
    'cardholder': "FirstName LastName",
    'exp_m': "12",  # 2 digits
    'exp_y': "20",  # 4 digits
    'cvv': "666"  # 3 digits
}
