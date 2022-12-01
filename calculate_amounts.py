import datetime

# calculate revenue amount within given dates
def GetRevenue(fDateStart, fDateEnd, fListSold):
    tmpTotal = 0
    for obj_sold in fListSold:
        if (obj_sold.sell_date >= datetime.datetime.strftime(fDateStart, "%Y-%m-%d")) and \
            (obj_sold.sell_date <= datetime.datetime.strftime(fDateEnd, "%Y-%m-%d")):
            tmpTotal = tmpTotal + float(obj_sold.sell_price)
    return tmpTotal

# calculate profit amount within given dates
def GetProfit(fDateStart, fDateEnd, fListBought, fListSold):
    tmpBought = 0
    tmpSold = 0
    for obj_sold in fListSold:
        if (obj_sold.sell_date >= datetime.datetime.strftime(fDateStart, "%Y-%m-%d")) and \
            (obj_sold.sell_date <= datetime.datetime.strftime(fDateEnd, "%Y-%m-%d")):
            tmpSold = tmpSold + float(obj_sold.sell_price)
            for obj_bought in fListBought:
                if (obj_bought.id == obj_sold.bought_id):
                    tmpBought = tmpBought + float(obj_bought.buy_price)
    return (tmpSold - tmpBought)
