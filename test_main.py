# how to run this test:
#   (first, navigate to the superpy directory)
#   python -m pytest test_main.py

import main
import classes
import constants
import inventory
import datetime
import current_date
import helpers

# create a number of Bought rows (and do some checks on a few fields)
def test_current_date():
    pass

def test_bought():
    main.list_bought.clear()
    main.list_bought.append(classes.Bought(-1, "appels", "2022-10-05", 1.50, "2022-10-10", main.list_bought))
    main.list_bought.append(classes.Bought(-1, "peren", "2022-10-02", 3.15, "2022-10-05", main.list_bought))
    main.list_bought.append(classes.Bought(-1, "kiwi", "2022-10-12", 79.00, "2022-10-13", main.list_bought))
    main.list_bought.append(classes.Bought(-1, "appels", "2022-10-07", 2.50, "2022-10-18", main.list_bought))
    main.list_bought.append(classes.Bought(-1, "appels", "2022-10-05", 1.50, "2022-10-10", main.list_bought))
    main.list_bought.append(classes.Bought(-1, "appels", "2022-10-05", 1.50, "2022-10-10", main.list_bought))

    assert main.list_bought[0].product_name == "appels"
    assert main.list_bought[0].buy_price    == 1.50

# create a number of Sold rows (and do some checks on a few fields)
def test_sold():
    main.list_sold.clear()
    main.list_sold.append(classes.Sold(-1, "kiwi", "2022-10-05", 2.50, main.list_sold))
    main.list_sold.append(classes.Sold(-1, "appels", "2022-10-02", 4.15, main.list_sold))
    main.list_sold.append(classes.Sold(-1, "appels", "2022-10-04", 4.25, main.list_sold))

    assert main.list_sold[0].sell_price == 2.50
    assert main.list_sold[1].sell_date == '2022-10-02'
    assert main.list_sold[2].sell_price == 4.25
