import os

TEST_MODE = False # for testing purposes set this to True for additional output

FIELDS_BOUGHT = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]
FIELDS_SOLD = ["id", "bought_id", "sell_date", "sell_price"]
FIELDS_INVENTORY = ["product_name", "count", "buy_price", "expiration_date"]
FILE_BOUGHT = "bought.csv"
FILE_SOLD = "sold.csv"
FILE_CURRENT_DATE = "current_date_.txt"
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\" + "data" + "\\"

CYAN = "#00FFFF"
RED = "#FF0000"
GREEN = "#00FF00"
ORANGE = "#FFA500"
NAVY = "#000080"
MAGENTA = "#FF00FF"
OLIVE = "#808000"
YELLOW = "#FFFF00"
PURPLE = "#A020F0"
GRAY = "#808080"
BURGUNDY = "#8B0000"
PINK = "#AA336A"