import locale
import csv
import os.path
from rich.console import Console
from rich.table import Table

# return the ID of the first available Bought row, when not available then return value -1
def GetBoughtId(fProductName, fListBought, fListSold):
    tmpResult = -1
    for obj_bought in fListBought:
        if obj_bought.product_name.lower() == fProductName.lower():
            tmpFound = False
            for obj_sold in fListSold:
                if obj_sold.bought_id == obj_bought.id:
                    tmpFound = True
            if tmpFound == False:
                tmpResult = obj_bought.id
                break # don't go searching further, just use the first available row!
    return tmpResult

# add prefix zeros
def ExtraZero(fInt):
    if fInt < 10:
        return "0" + str(fInt)
    else:
        return str(fInt)

# format money in Dutch format, e.g. € 1.999,95
def FormatMoney(fValue):
    locale.setlocale(locale.LC_ALL, '') # use the settings of the user's operating system
    tmpMoneyStr = locale.currency(fValue, grouping=True)
    return tmpMoneyStr

# check if file exists and, if not, then create new file
def CreateFileIfNotExists(fFilename, fHeader):
    if not os.path.exists(fFilename):
        with open(fFilename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=";")
            csvwriter.writerow(fHeader)

# generic method for printing data in table by using rich.console       
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
