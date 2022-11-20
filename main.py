# Imports
import argparse
import csv
import os
import os.path
import locale
import datetime
import matplotlib.pyplot as plt
from calendar import monthrange
from tabulate import tabulate
from rich.console import Console
from rich.table import Table

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
list_bought = []
list_sold = []
list_inventory = []
report_date = "1900-01-01"

TEST_MODE = False
FIELDS_BOUGHT = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]
FIELDS_SOLD = ["id", "bought_id", "sell_date", "sell_price"]
FIELDS_INVENTORY = ["product_name", "count", "buy_price", "expiration_date"]
FILE_BOUGHT = "bought.csv"
FILE_SOLD = "sold.csv"
FILE_CURRENT_DATE = "current_date_.txt"
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\" + "data" + "\\"
START_ID_BOUGHT = 1000
START_ID_SOLD = 5000

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

class Bought:
    def __init__(self, id, product_name, buy_date, buy_price, expiration_date):
        if id == -1:
            self.id = GetNewId(START_ID_BOUGHT, list_bought)
        else:
            self.id = id
        self.product_name = product_name
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.expiration_date = expiration_date

class Sold:
    def __init__(self, id, bought_id, sell_date, sell_price):
        if id == -1:
            self.id = GetNewId(START_ID_SOLD, list_sold)
        else:
            self.id = id
        self.bought_id = bought_id
        self.sell_date = sell_date
        self.sell_price = sell_price

class Inventory:
    def __init__(self, product_name, count, buy_price, expiration_date):
        self.product_name = product_name
        self.count = count
        self.buy_price = buy_price
        self.expiration_date = expiration_date

def GetNewId(fId, fList):
    fNewId = fId
    for obj in fList:
        for key, value in obj.__dict__.items():
            if key == "id":
                if int(value) > fNewId:
                    fNewId = int(value)
    fNewId = fNewId + 1
    return fNewId

def GetBoughtId(fProductName):
    tmpResult = -1
    for obj_bought in list_bought:
        if obj_bought.product_name == fProductName:
            tmpFound = False
            for obj_sold in list_sold:
                if obj_sold.bought_id == obj_bought.id:
                    tmpFound = True
            if tmpFound == False:
                tmpResult = obj_bought.id
                break
    return tmpResult

def calculate_inventory_list(fDate):
    list_inventory.clear()
    for obj_bought in list_bought:
        # kijk alleen naar producten die voor/op peildatum zijn ingekocht        
        if obj_bought.buy_date <= datetime.datetime.strftime(fDate, "%Y-%m-%d"):
            # controleer of product nog NIET is verkocht voor/op peildatum
            tmpSold = False
            for obj_sold in list_sold:
                if (obj_sold.bought_id == obj_bought.id) and \
                    (obj_sold.sell_date <= datetime.datetime.strftime(fDate, "%Y-%m-%d")):
                    tmpSold = True
            # indien product nog NIET verkocht dan toevoegen op voorraadlijst
            if tmpSold == False: 
                # indien zelfde artikel (zelfde naam, prijs, exp.datum) al voorkomt, dan alleen aantal ophogen bestaande regel    
                tmpAdded = False
                for obj_inventory in list_inventory:
                    if (obj_bought.product_name == obj_inventory.product_name) and \
                        (obj_bought.buy_price == obj_inventory.buy_price) and \
                        (obj_bought.expiration_date == obj_inventory.expiration_date):
                        obj_inventory.count = obj_inventory.count + 1
                        tmpAdded = True
                # indien nog geen aantal is verhoogd dan moet er een nieuwe voorraadregel worden aangemaakt
                if tmpAdded == False:
                    list_inventory.append(Inventory(obj_bought.product_name, 1, obj_bought.buy_price, obj_bought.expiration_date))

def GetRevenue(fDateStart, fDateEnd):
    tmpTotal = 0
    for obj_sold in list_sold:
        if (obj_sold.sell_date >= datetime.datetime.strftime(fDateStart, "%Y-%m-%d")) and \
            (obj_sold.sell_date <= datetime.datetime.strftime(fDateEnd, "%Y-%m-%d")):
            tmpTotal = tmpTotal + float(obj_sold.sell_price)
    return tmpTotal

def GetProfit(fDateStart, fDateEnd):
    tmpBought = 0
    tmpSold = 0
    for obj_sold in list_sold:
        if (obj_sold.sell_date >= datetime.datetime.strftime(fDateStart, "%Y-%m-%d")) and \
            (obj_sold.sell_date <= datetime.datetime.strftime(fDateEnd, "%Y-%m-%d")):
            tmpSold = tmpSold + float(obj_sold.sell_price)
            for obj_bought in list_bought:
                if (obj_bought.id == obj_sold.bought_id):
                    tmpBought = tmpBought + float(obj_bought.buy_price)
    return (tmpSold - tmpBought)

def LoadReportDateFromFile():
    global report_date
    CreateFileIfNotExists(FILE_CURRENT_DATE, [datetime.datetime.today().strftime("%Y-%m-%d")])
    with open(DIR_PATH + FILE_CURRENT_DATE) as f:
        tmpLines = f.readlines()
    report_date = tmpLines[0].strip()

def SaveReportDateToFile(fAdvanceTime):
    tmpToday = datetime.datetime.now()
    tmpNewDate = tmpToday + datetime.timedelta(days=fAdvanceTime)
    with open(DIR_PATH + FILE_CURRENT_DATE, 'w') as f:
        f.write(tmpNewDate.strftime("%Y-%m-%d"))

def export_to_csv(fFilename, fFields, fObjList):
    with open(DIR_PATH + fFilename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        csvwriter.writerow(fFields)
        for obj in fObjList:
            row = []
            for key, value in obj.__dict__.items():
                row.append(str(value))
            csvwriter.writerow(row)

def import_bought_from_csv(fFilename):
    CreateFileIfNotExists(fFilename, FIELDS_BOUGHT)
    list_bought.clear()
    with open(DIR_PATH + fFilename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
        for row in csvreader:
            list_bought.append(Bought(row[0], row[1], row[2], row[3], row[4]))

def import_sold_from_csv(fFilename):
    CreateFileIfNotExists(fFilename, FIELDS_SOLD)
    list_sold.clear()
    with open(DIR_PATH + fFilename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        fields = next(csvreader)
        for row in csvreader:
            list_sold.append(Sold(row[0], row[1], row[2], row[3]))

def CreateFileIfNotExists(fFilename, fHeader):
    if not os.path.exists(DIR_PATH + fFilename):
        with open(DIR_PATH + fFilename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=";")
            csvwriter.writerow(fHeader)
          
def print_table(fTitle, fObjList, fFields):
    console = Console()
    table = Table(title=fTitle, show_header=True, header_style="bold magenta")
    for fField in fFields:
        tmpStyle = "white"
        tmpJustify = "left"
        if ('count' in fField) or ('date' in fField): 
            tmpJustify = 'center'
        if ('price' in fField):
            tmpJustify = 'right'
            tmpStyle = 'green'   
        if (fField == 'id'): 
            tmpStyle = 'blue'         
        table.add_column(fField, style=tmpStyle, justify=tmpJustify)
    for obj in fObjList:
        fList = []
        for key, value in obj.__dict__.items():
            if 'price' in key:
                fList.append(FormatMoney(float(value)))
            else:
                fList.append(str(value))
        table.add_row(*fList)
    console.print(table)

def ExtraZero(fInt):
    if fInt < 10:
        return "0" + str(fInt)
    else:
        return str(fInt)

def GetGraphList(fYear):
    tmpList = []
    for tmpMonth in range(1, 13):
        tmpTotal = 0
        for obj_sold in list_sold:
            tmpFirstDay = str(fYear) + "-" + ExtraZero(tmpMonth) + "-01"
            tmpLastDay  = str(fYear) + "-" + ExtraZero(tmpMonth) + "-" + str(monthrange(fYear, tmpMonth)[1])
            if (obj_sold.sell_date >= tmpFirstDay) and (obj_sold.sell_date <= tmpLastDay): 
                tmpTotal = tmpTotal + float(obj_sold.sell_price)
        tmpList.append(tmpTotal)
    return tmpList

def ShowRevenueGraph(fYear):
    fig, ax = plt.subplots()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    counts = GetGraphList(fYear)
    
    bar_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
    bar_colors = [CYAN, RED, GREEN, ORANGE, NAVY, MAGENTA, OLIVE, YELLOW, PURPLE, GRAY, BURGUNDY, PINK]

    ax.bar(months, counts, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Revenue (EUR)") 
    ax.set_title("Revenue " + str(fYear)) 
 
    plt.show()

def FormatMoney(fValue):
    locale.setlocale(locale.LC_ALL, "nl_NL")
    tmpMoneyStr = locale.currency(fValue, grouping=True)
    return tmpMoneyStr

def buy(args):
    import_bought_from_csv(FILE_BOUGHT)
    tmpProductName = vars(args)['product_name']
    tmpBuyDate = datetime.datetime.now().strftime("%Y-%m-%d")
    tmpBuyPrice = vars(args)['price']
    tmpExpirationDate = datetime.datetime.strftime(datetime.datetime.strptime(vars(args)['expiration_date'], "%Y-%m-%d"), "%Y-%m-%d")
    list_bought.append(Bought(-1, tmpProductName, tmpBuyDate, tmpBuyPrice, tmpExpirationDate))
    export_to_csv(FILE_BOUGHT, FIELDS_BOUGHT, list_bought)
    if TEST_MODE == True:
        print_table('bought', list_bought, FIELDS_BOUGHT)
    else:
        print("OK")

def sell(args):
    import_bought_from_csv(FILE_BOUGHT)
    import_sold_from_csv(FILE_SOLD)
    tmpBoughtId = int(GetBoughtId(vars(args)['product_name']))
    if tmpBoughtId > 0:
        tmpSellDate = datetime.datetime.now().strftime("%Y-%m-%d")
        tmpSellPrice = vars(args)['price']
        list_sold.append(Sold(-1, tmpBoughtId, tmpSellDate, tmpSellPrice))
        export_to_csv(FILE_SOLD, FIELDS_SOLD, list_sold)
        if TEST_MODE == True:
            print_table('bought', list_bought, FIELDS_BOUGHT)
            print_table('sold', list_sold, FIELDS_SOLD)
        else:
            print("OK")
    else:
        print("ERROR: Product not in stock.")

def report(args):
    import_bought_from_csv(FILE_BOUGHT)
    import_sold_from_csv(FILE_SOLD)
    LoadReportDateFromFile()
    
    tmpReportType = vars(args)['report-type']
    tmpNowYN = vars(args)['now']
    tmpTodayYN = vars(args)['today']
    tmpYesterdayYN = vars(args)['yesterday']
    if vars(args)['date'] is not None:
        tmpDate = datetime.datetime.strptime(str(vars(args)['date']), "%Y-%m-%d")

    if (tmpNowYN == True) or (tmpTodayYN == True):
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(report_date, "%Y-%m-%d")
        tmpRevenueLine = "Today's revenue so far: "
        tmpProfitLine = "Today's profit so far: "
        
    if (tmpYesterdayYN == True):
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(report_date, "%Y-%m-%d") - datetime.timedelta(days=1)
        tmpRevenueLine = "Yesterday's revenue: "
        tmpProfitLine = "Yesterday's profit: "
        
    if vars(args)['date'] is not None:
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(vars(args)['date'], "%Y-%m-%d")
        tmpRevenueLine = "Revenue from " + datetime.datetime.strftime(tmpDate, "%Y-%m-%d") + " "
        tmpProfitLine = "Profit from " + datetime.datetime.strftime(tmpDate, "%Y-%m-%d") + " "
        
    if tmpReportType == 'inventory':
        calculate_inventory_list(tmpDateEnd)
        print_table('inventory', list_inventory, FIELDS_INVENTORY)

    if tmpReportType == 'revenue':
        print(tmpRevenueLine + FormatMoney(GetRevenue(tmpDateStart, tmpDateEnd)))
    
    if tmpReportType == 'profit':
        print(tmpProfitLine + FormatMoney(GetProfit(tmpDateStart, tmpDateEnd)))

def graph(args):
    import_sold_from_csv(FILE_SOLD)
    tmpYear = vars(args)['year']
    ShowRevenueGraph(tmpYear)

def main_parser():
    parser = argparse.ArgumentParser(description='Welcome to the SuperPy command line parser')
    subparsers = parser.add_subparsers(dest='main_command', help='main command')
    parser.add_argument('-a', '--advance-time', type=int)

    a_parser = subparsers.add_parser('buy', help='buy product and add to inventory')
    a_parser.add_argument('-n', '--product-name', type=str, required=True)
    a_parser.add_argument('-p', '--price', type=float, required=True)
    a_parser.add_argument('-e', '--expiration-date', type=str, required=True)
    a_parser.set_defaults(func=buy)

    b_parser = subparsers.add_parser('sell', help='sell product and remove from inventory')
    b_parser.add_argument('-n', '--product-name', type=str, required=True)
    b_parser.add_argument('-p', '--price', type=float, required=True)
    b_parser.set_defaults(func=sell)

    c_parser = subparsers.add_parser('report', help='show management report')
    c_parser.add_argument('report-type', choices=['inventory', 'revenue', 'profit'], help='type of report')
    c_group = c_parser.add_mutually_exclusive_group(required=True)
    c_group.add_argument('-n', '--now', action='store_true')
    c_group.add_argument('-t', '--today', action='store_true')
    c_group.add_argument('-y', '--yesterday', action='store_true')
    c_group.add_argument('-d', '--date', type=str) 
    c_parser.set_defaults(func=report)

    d_parser = subparsers.add_parser('graph', help='show revenue graph')
    d_parser.add_argument('-y', '--year', type=int, required=True)
    d_parser.set_defaults(func=graph)

    args = parser.parse_args()
    if (vars(args)["advance_time"] is not None):
        SaveReportDateToFile(vars(args)["advance_time"])
    if (vars(args)["main_command"] is not None):
        args.func(args)

if __name__ == "__main__":
    main_parser()





