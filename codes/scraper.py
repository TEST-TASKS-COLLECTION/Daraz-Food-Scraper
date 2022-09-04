from unicodedata import name
import requests
from bs4 import BeautifulSoup as bs
import json
import argparse
import re
import csv


PATTERN = r"^([A-Za-z ]*)(?:- )*([0-9]+)([ g|kg|gm|ml|l|ltr]*)"

def get_product():
    """
    return user provided terminal argument
    """
    parser = argparse.ArgumentParser(description="A Daraz food product scraper")
    parser.add_argument("--prod", help="Food Product Name")
    args = parser.parse_args()
    return args.prod
    
def unit_parser(item):
    patt = re.compile(PATTERN)
    d = patt.findall(item['name'].lower())
    if not d:
        return 
    if d[0][0]:
        return_dict = {
            "name": d[0][0],
            "amount": d[0][1],
            "unit": d[0][2],
        }
        return standarize_unit(return_dict)


def standarize_unit(item):
    if item['unit'] in ['ml']:
        item['amount'] = str(int(item['amount']) / 1000)
        item['unit'] = "l"
    elif item['unit'] in ['g', 'gm']:
        item['amount'] = str(int(item['amount']) / 1000)
        item['unit'] = "kg"
    
    return item

class DarazScraper:
    
    def __init__(self, query):
        self.query = query
        self.url = f'https://www.daraz.com.np/catalog/?ajax=true&q={query}'
    
    def get_request_json(self):
        res = requests.get(self.url).json()
        return res['mods']['listItems']
    
    
    def save_data(self, data):
        with open(f"data/{self.query}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['Product', 'Quantity', "Unit"])
            for item in data:
                print(item)
                writer.writerow([item["name"].strip(), item["amount"].strip(), item["unit"].strip()])
    
    def get_data(self):
        """
        Returns:
            items (list): list of tuples containing the item name and its quantity  
        """
        data = self.get_request_json()
        
        items = [unit_parser(i) for i in data if unit_parser(i)]
        # items = [patt.findall(i['name'].lower()) for i in data if patt.findall(i['name'])]
        print(items)
        self.save_data(items)
        return items
            # print(item.name)
        # return soup.select_one(".title--wFj93")


if __name__ == "__main__":
    product = get_product()
    data = DarazScraper(product).get_data()