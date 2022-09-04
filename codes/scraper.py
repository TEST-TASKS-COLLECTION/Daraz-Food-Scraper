import requests
from bs4 import BeautifulSoup as bs
import json
import argparse

def get_product():
    """
    return user provided terminal argument
    """
    parser = argparse.ArgumentParser(description="A Daraz food product scraper")
    parser.add_argument("--prod", help="Food Product Name")
    args = parser.parse_args()
    return args.prod


class DarazScraper:
    
    def __init__(self, query):
        self.url = f'https://www.daraz.com.np/catalog/?q={query}'
    
    def get_request_json(self):
        res = requests.get(self.url).text
        # return res
        soup = bs(res, 'html.parser') 
        for data in soup.find_all("script"):
            if "window.pageData" in data.text:
                # print(data.text)
                data = data.text.replace("window.pageData=", "")
                break
        # print(data)
        return json.loads(data)['mods']['listItems']
    
    def get_data(self):
        data = self.get_request_json()
        for item in data:
            print(item['name'])
            # print(item.name)
        # return soup.select_one(".title--wFj93")


if __name__ == "__main__":
    product = get_product()
    data = DarazScraper(product).get_data()