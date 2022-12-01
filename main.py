# Imports
import argparse
import datetime
import calculate_amounts
import classes
import constants
import current_date
import graphs
import helpers
import import_and_export
import inventory

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
list_bought = []
list_sold = []
list_inventory = []

# argparser: buy function
def buy(args):
    import_and_export.import_from_csv(constants.FILE_BOUGHT, constants.FIELDS_BOUGHT, list_bought)
    tmpProductName = vars(args)['product_name']
    current_date.LoadReportDateFromFile()
    tmpBuyDate = current_date.report_date
    tmpBuyPrice = vars(args)['price']
    tmpExpirationDate = datetime.datetime.strftime(datetime.datetime.strptime(vars(args)['expiration_date'], "%Y-%m-%d"), "%Y-%m-%d")
    list_bought.append(classes.Bought(-1, tmpProductName, tmpBuyDate, tmpBuyPrice, tmpExpirationDate, list_bought))
    import_and_export.export_to_csv(constants.FILE_BOUGHT, constants.FIELDS_BOUGHT, list_bought)
    if constants.TEST_MODE == True:
        helpers.print_table('bought', list_bought, constants.FIELDS_BOUGHT)
    else:
        print("Product bought on: " + tmpBuyDate)

# argparser: sell function
def sell(args):
    import_and_export.import_from_csv(constants.FILE_BOUGHT, constants.FIELDS_BOUGHT, list_bought)
    import_and_export.import_from_csv(constants.FILE_SOLD, constants.FIELDS_SOLD, list_sold)
    tmpBoughtId = int(helpers.GetBoughtId(vars(args)['product_name'], list_bought, list_sold))
    if tmpBoughtId > 0:
        current_date.LoadReportDateFromFile()
        tmpSellDate = current_date.report_date
        tmpSellPrice = vars(args)['price']
        list_sold.append(classes.Sold(-1, tmpBoughtId, tmpSellDate, tmpSellPrice, list_sold))
        import_and_export.export_to_csv(constants.FILE_SOLD, constants.FIELDS_SOLD, list_sold)
        if constants.TEST_MODE == True:
            helpers.print_table('bought', list_bought, constants.FIELDS_BOUGHT)
            helpers.print_table('sold', list_sold, constants.FIELDS_SOLD)
        else:
            print("Product sold on: " + tmpSellDate)
    else:
        print("ERROR: Product not in stock.")

# argparser: report function (inventory, revenue, report)
def report(args):
    import_and_export.import_from_csv(constants.FILE_BOUGHT, constants.FIELDS_BOUGHT, list_bought)
    import_and_export.import_from_csv(constants.FILE_SOLD, constants.FIELDS_SOLD, list_sold)
    current_date.LoadReportDateFromFile()

    tmpReportType = vars(args)['report-type']
    tmpNowYN = vars(args)['now']
    tmpTodayYN = vars(args)['today']
    tmpYesterdayYN = vars(args)['yesterday']
    if vars(args)['date'] is not None:
        tmpDate = datetime.datetime.strptime(str(vars(args)['date']), "%Y-%m-%d")

    if (tmpNowYN == True) or (tmpTodayYN == True):
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(current_date.report_date, "%Y-%m-%d")
        tmpRevenueLine = "Today's revenue so far: "
        tmpProfitLine = "Today's profit so far: "
        
    if (tmpYesterdayYN == True):
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(current_date.report_date, "%Y-%m-%d") - datetime.timedelta(days=1)
        tmpRevenueLine = "Yesterday's revenue: "
        tmpProfitLine = "Yesterday's profit: "
        
    if vars(args)['date'] is not None:
        tmpDateStart = tmpDateEnd = datetime.datetime.strptime(vars(args)['date'], "%Y-%m-%d")
        tmpRevenueLine = "Revenue from " + datetime.datetime.strftime(tmpDate, "%Y-%m-%d") + " "
        tmpProfitLine = "Profit from " + datetime.datetime.strftime(tmpDate, "%Y-%m-%d") + " "
        
    if tmpReportType == 'inventory':
        inventory.calculate_inventory_list(tmpDateEnd, list_bought, list_sold, list_inventory)
        helpers.print_table('inventory', list_inventory, constants.FIELDS_INVENTORY)

    if tmpReportType == 'revenue':
        print(tmpRevenueLine + helpers.FormatMoney(calculate_amounts.GetRevenue(tmpDateStart, tmpDateEnd, list_sold)))
    
    if tmpReportType == 'profit':
        print(tmpProfitLine + helpers.FormatMoney(calculate_amounts.GetProfit(tmpDateStart, tmpDateEnd, list_bought, list_sold)))

# argparser: graph function
def graph(args):
    import_and_export.import_from_csv(constants.FILE_SOLD, constants.FIELDS_SOLD, list_sold)
    tmpYear = vars(args)['year']
    graphs.ShowRevenueGraph(tmpYear, list_sold)

# argparser: main
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
        current_date.SaveReportDateToFile(vars(args)["advance_time"])
        current_date.LoadReportDateFromFile() # after saving new date to file, reload value into current_date.report_date
        print("Current date set to: " + current_date.report_date)
    if (vars(args)["main_command"] is not None):
        args.func(args)

# starting point for program
if __name__ == "__main__":
    main_parser()
