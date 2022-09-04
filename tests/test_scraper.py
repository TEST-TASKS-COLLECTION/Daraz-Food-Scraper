from codes.scraper import unit_parser, DarazScraper, read_data
import os

PARSE_PATH = 'data/oil.csv'
PROCESS_PATH = "data/oil_std.csv"

def setUp():
    if os.path.isfile(PARSE_PATH):
        os.remove(PARSE_PATH)
    if os.path.isfile(PROCESS_PATH):
        os.remove(PROCESS_PATH)
    DarazScraper("oil")

def test_unit():
    item1 = {"name": "Gyan Basmati Rice Premium 20kg"}
    item2 = {"name": "Sara Foods Sama Rice - 500gm"}
    item3 = {"name": "Sara Foods Cold Pressed Sesame Oil 100ml"}
    item4 = {"name": "dhara mustard oil 1 ltr"}
    assert unit_parser(item1, True)['unit'] == "gm"
    assert unit_parser(item1, True)['amount'] == "20000.0"
    
    assert unit_parser(item2)['unit'] == "gm"
    assert unit_parser(item2)['amount'] == "500"
    
    assert unit_parser(item3)['unit'] == "ml"
    assert unit_parser(item3)['amount'] == "100"
    
    assert unit_parser(item4, True)['unit'] == "ml"
    assert unit_parser(item4, True)['amount'] == "1000.0"
    
def test_name():
    item1 = {"name": "Gyan Basmati Rice Premium 20kg"}
    item3 = {"name": "Sara Foods Cold Pressed Sesame Oil 100ml"}
    assert unit_parser(item1)['name'] == "Gyan Basmati Rice Premium"
    assert unit_parser(item3)['name'] == "Sara Foods Cold Pressed Sesame Oil"

def test_parser_creates_file():
    setUp()
    assert os.path.isfile(PARSE_PATH)
    assert os.path.isfile(PROCESS_PATH)

# def 

def test_parser_run_same_output():
    setUp()
    parse_op = read_data(PARSE_PATH)
    process_op = read_data(PROCESS_PATH)
    assert len(parse_op) == len(process_op)
