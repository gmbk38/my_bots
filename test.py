from urllib.parse import quote
from urllib.parse import unquote
import random

url = "https://steamcommunity.com/market/listings/730/Desert Eagle | Night (Well-Worn)"

encoded_url = quote(url, safe=':/')

print(encoded_url)
print('https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Night%20%28Well-Worn%29')
print(unquote(encoded_url))

# proxies = [
#     {"http": "http://203.22.223.211:80",
#     "https": "http://203.22.223.211:80"},
#     {"http": "http://203.28.8.219:80",
#     "https": "http://203.28.8.219:80"},
#     {"http": "http://203.24.102.226:80",
#     "https": "http://203.24.102.226:80"},
#     {"http": "http://203.32.121.234:80",
#     "https": "http://203.32.121.234:80"},
#     {"http": "http://45.12.30.242:80",
#     "https": "http://45.12.30.242:80"},
#     {"http": "http://203.30.190.254:80",
#     "https": "http://203.30.190.254:80"},
#     {"http": "http://203.23.103.96:80",
#     "https": "http://203.23.103.96:80"},
#     {"http": "http://203.23.103.31:80",
#     "https": "http://203.23.103.31:80"},    
# ]

# print(random.choice(proxies))