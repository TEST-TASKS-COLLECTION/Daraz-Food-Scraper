from codes.scraper import unit_parser


def test_unit_parser():
    item1 = {"name": "Gyan Basmati Rice Premium 20kg"}
    item2 = {"name": "Sara Foods Sama Rice - 500gm"}
    item3 = {"name": "Sara Foods Cold Pressed Sesame Oil 100ml"}
    assert unit_parser(item1)[0][1] == "20kg"
    assert unit_parser(item2)[0][1] == "500gm"
    assert unit_parser(item3)[0][1] == "100ml"
    