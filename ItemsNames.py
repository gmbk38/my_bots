import requests
from bs4 import BeautifulSoup

def getItemsNames(*args):

    items_names = []

    for items_type in args:

        url = f'https://wiki.cs.money/weapons/{items_type.lower()}'

        headers = {
            'Referer' : 'https://wiki.cs.money/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
        }

        float_values = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']

        response = requests.get(url, headers)

        if (response.status_code != 200):
            print ('Ошибка получения items name')

        soup = BeautifulSoup(response.text, 'html.parser')
        for el in soup.findAll('div',{'class':'zhqwubnajobxbgkzlnptmjmgwn'})[15::]:
            for fv in float_values:
                items_names.append(f'{items_type} | {el.getText()} ({fv})')

    return items_names