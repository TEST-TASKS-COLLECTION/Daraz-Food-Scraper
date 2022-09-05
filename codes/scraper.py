from unicodedata import name
import os
import requests
from bs4 import BeautifulSoup as bs
import json
import argparse
import re
import csv


PATTERN = r"^([A-Za-z '()&_-]*)(?:[\W|\b|]*)*([0-9]+)(?:[\W]*)*([g|kg|gm|ml|l|ltr]*)"
# PATTERN = r"^([A-Za-z '()&_-]*)(?:[\W|\b|]*)*([0-9]+)(?:[\W]*)*([g|kg|gm|ml|l|ltr|L|Kg|G]*)"
# UNITS = ["g", "kg", "gm", "ml", "l", "ltr", "L", "Kg", "G"]

def standarize_unit(item):
    """

    Args:
        item (dict): a dictionary of not standarized input item

    Returns:
        item (dict): a dictionary of standarized item
    """
    if item['unit'] in ['l', 'ltr']:
        item['amount'] = item['amount'] * 1000
        item['unit'] = "ml"
    elif item['unit'] in ['kg']:
        item['amount'] = item['amount'] * 1000
        item['unit'] = "gm"
    elif item['unit'] in ['g']:
        item['unit'] = "gm"
    
    return item

def get_product():
    """
    return user provided terminal argument
    """
    parser = argparse.ArgumentParser(description="A Daraz food product scraper")
    parser.add_argument("--prod", help="Food Product Name")
    parser.add_argument("--mode", help="Mode to run your program (extract, transform, run(default, extract + transform)", default="run")
    args = parser.parse_args()
    return args.prod, args.mode
    
def unit_parser(item):
    """
    Gets a product name and returns a standarized dictionary of an item
    Args:
        item (str): an items name
    """
    patt = re.compile(PATTERN)
    d = patt.findall(item['name'].lower())
    if not d:
        return 
    if d[0][0] and d[0][2]:
        return_dict = {
            "name": d[0][0].replace("-", "").replace("(", "").strip().title(),
            "amount": float(d[0][1]),
            "unit": d[0][2].strip(),
        }
        # if not standarize:
        #     return return_dict
        return standarize_unit(return_dict)

def save_data(path, data, cols):
    with open(path, "w") as f:
        writer = csv.writer(f)
        # writer.writerow(['Product', 'Quantity', "Unit"])
        writer.writerow(cols)
        if len(cols) == 3:
            for item in data:
                # print(item)
                writer.writerow([item["name"].strip(), str(float(item["amount"])).strip(), item["unit"].strip()])
        elif len(cols) == 1:
            for item in data:
                writer.writerow([item.strip()])
        else:
            print("Incorrect format")

def read_data(path):
        items = []
        try:
            with open(path) as f:
                next(f)
                r = csv.reader(f)
                for i in r:
                    items.append({
                        "name": i[0].strip()
                    })
            return items
        except FileNotFoundError:
            print("File doesn't exist try running in extract mode or run mode")




class DarazScraper:
    
    
    def __init__(self, query, mode="run"):
        self.query = query
        self.url = f'https://www.daraz.com.np/catalog/?ajax=true&q={query}'
        self.parse_path = f"data/{query}.csv"
        self.process_path = f"data/{query}_std.csv"
        getattr(self, mode)()
    
    def get_request_json(self):
        res = requests.get(self.url).json()
        return res['mods']['listItems']
        
    def extract(self):
        """
        extract the required data from the web and saves it (if that file isn't extracted already) 
        """
        if not os.path.isfile(self.parse_path):
            data = self.get_request_json()
            items = [i['name'] for i in data if any(d.isdigit() for d in i["name"])]
            path = self.parse_path
            save_data(path, items, cols=["Product"])
        else:
            print("PRODUCT ALREADY EXISTS NO NEED TO SCRAP")

    def transform(self):
        """
        loads the data and transforms it into a clean format and save into a new file 
        """
        items = read_data(self.parse_path)
        if items:
            items = [unit_parser(i) for i in items if unit_parser(i)]
            # items = [standarize_unit(item) for item in items]
            
            path = self.process_path
            save_data(path=path, data = items, cols=['Product', 'Quantity', "Unit"])

    def run(self):
        """
        Runs both extract and transform function sequentially
        """
        self.extract()
        self.transform()


if __name__ == "__main__":
    product, mode = get_product()
    # scrape(product)
    # process(product)
    scraper = DarazScraper(product, mode)