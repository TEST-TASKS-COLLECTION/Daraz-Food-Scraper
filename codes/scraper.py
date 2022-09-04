import requests
from bs4 import BeautifulSoup as bs
import json
import argparse
import re
import csv


PATTERN = r"^([A-Za-z ]*)(?:- )*([0-9]+[ g|kg|gm|ml|l|ltr]+)"

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
        self.query = query
        self.url = f'https://www.daraz.com.np/catalog/?ajax=true&q={query}'
    
    def get_request_json(self):
        res = requests.get(self.url).json()
        return res['mods']['listItems']
    
    
    def save_data(self, items):
        with open(f"data/{self.query}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['Product', 'Quantity'])
            for item in items:
                print(item)
                writer.writerow([item[0][0].strip(), item[0][1].strip()])
    
    def unit_parser(self, item):
        patt = re.compile(PATTERN)
        d = patt.findall(item['name'].lower())
        if not d:
            return 
        if d[0][0]:
            return d
    
    def get_data(self):
        """
        Returns:
            items (list): list of tuples containing the item name and its quantity  
        """
        data = self.get_request_json()
        
        items = [self.unit_parser(i) for i in data if self.unit_parser(i)]
        # items = [patt.findall(i['name'].lower()) for i in data if patt.findall(i['name'])]
        
        self.save_data(items)
        return items
            # print(item.name)
        # return soup.select_one(".title--wFj93")


if __name__ == "__main__":
    product = get_product()
    data = DarazScraper(product).get_data()