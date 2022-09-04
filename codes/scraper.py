import requests
from bs4 import BeautifulSoup as bs
import json
import argparse
import re
import csv


PATTERN = r"^([A-Za-z ]*)(?:- )*([0-9]+.*)"

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
    
    
    def save_data(self, items):
        with open("data/items.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['Product', 'Quantity'])
            for item in items:
                print(item)
                writer.writerow([item[0][0].strip(), item[0][1]])
    
    def get_data(self):
        """

        Returns:
            items (list): list of tuples containing the item name and its quantity  
        """
        data = self.get_request_json()
        patt = re.compile(PATTERN)
        items = [patt.findall(i['name']) for i in data if patt.findall(i['name'])]
        
        self.save_data(items)
        return items
            # print(item.name)
        # return soup.select_one(".title--wFj93")


if __name__ == "__main__":
    product = get_product()
    data = DarazScraper(product).get_data()