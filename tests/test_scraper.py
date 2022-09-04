from codes.scraper import unit_parser


def test_unit():
    item1 = {"name": "Gyan Basmati Rice Premium 20kg"}
    item2 = {"name": "Sara Foods Sama Rice - 500gm"}
    item3 = {"name": "Sara Foods Cold Pressed Sesame Oil 100ml"}
    item4 = {"name": "dhara mustard oil 1 ltr"}
    assert unit_parser(item1)['unit'] == "gm"
    assert unit_parser(item1)['amount'] == "20000"
    
    assert unit_parser(item2)['unit'] == "gm"
    assert unit_parser(item2)['amount'] == "500"
    
    assert unit_parser(item3)['unit'] == "ml"
    assert unit_parser(item3)['amount'] == "100"
    
    assert unit_parser(item4)['unit'] == "ml"
    assert unit_parser(item4)['amount'] == "1000"
    
def test_name():
    item1 = {"name": "Gyan Basmati Rice Premium 20kg"}
    item3 = {"name": "Sara Foods Cold Pressed Sesame Oil 100ml"}
    assert unit_parser(item1)['name'] == "Gyan Basmati Rice Premium"
    assert unit_parser(item3)['name'] == "Sara Foods Cold Pressed Sesame Oil"
    