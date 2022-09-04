from unicodedata import name
import os
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
    
def unit_parser(item, standarize=False):
    patt = re.compile(PATTERN)
    d = patt.findall(item['name'].lower())
    if not d:
        return 
    if d[0][0]:
        return_dict = {
            "name": d[0][0].strip().title(),
            "amount": d[0][1],
            "unit": d[0][2].strip(),
        }
        if not standarize:
            return return_dict
        return standarize_unit(return_dict)

def save_data(product, path, data):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(['Product', 'Quantity', "Unit"])
        for item in data:
            print(item)
            writer.writerow([item["name"].strip(), item["amount"].strip(), item["unit"].strip()])


def standarize_unit(item):
    print(item)
    if item['unit'] in ['l', 'ltr']:
        item['amount'] = str(float(item['amount']) * 1000)
        item['unit'] = "ml"
    elif item['unit'] in ['kg']:
        item['amount'] = str(float(item['amount']) * 1000)
        item['unit'] = "gm"
    
    return item

class DarazScraper:
    
    def __init__(self, query):
        self.query = query
        self.url = f'https://www.daraz.com.np/catalog/?ajax=true&q={query}'
    
    def get_request_json(self):
        res = requests.get(self.url).json()
        return res['mods']['listItems']
    
    

    def get_data(self, standarize=True):
        """
        Returns:
            items (list): list of tuples containing the item name and its quantity  
        """
        data = self.get_request_json()
        
        items = [unit_parser(i, standarize) for i in data if unit_parser(i)]
        # items = [patt.findall(i['name'].lower()) for i in data if patt.findall(i['name'])]
        print(items)
        path = f"data/{self.query}.csv"
        save_data(items, path)
        return items
            # print(item.name)
        # return soup.select_one(".title--wFj93")

def check_product_exists(product):
    if f"{product}.csv" in os.listdir('data'):
        print("PRODUCT ALREADY EXISTS NO NEED TO SCRAP")
        return True

    return False

def scrape(product):
    if not check_product_exists(product):
        DarazScraper(product, False)

def process(product):
    items = []
    with open(f"data/{product}.csv") as f:
        next(f)
        r = csv.reader(f)
        for i in r:
            items.append({
                "name": i[0].strip(),
                "amount": i[1],
                "unit": i[2].strip()
            })
    items = [standarize_unit(item) for item in items]
    
    path = f"data/{product}_std.csv"
    save_data(product, path, items)

def run(product, standarize=True):
        scrape(product)
        process(product)

if __name__ == "__main__":
    product = get_product()
    # scrape(product)
    # process(product)
    run(product)