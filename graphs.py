import constants
import helpers
import matplotlib.pyplot as plt
from calendar import monthrange

# generate list for showing graph data
def GetGraphList(fYear, fObjList):
    tmpList = []
    for tmpMonth in range(1, 13):
        tmpTotal = 0
        for obj_sold in fObjList:
            tmpFirstDay = str(fYear) + "-" + helpers.ExtraZero(tmpMonth) + "-01"
            tmpLastDay  = str(fYear) + "-" + helpers.ExtraZero(tmpMonth) + "-" + str(monthrange(fYear, tmpMonth)[1])
            if (obj_sold.sell_date >= tmpFirstDay) and (obj_sold.sell_date <= tmpLastDay): 
                tmpTotal = tmpTotal + float(obj_sold.sell_price)
        tmpList.append(tmpTotal)
    return tmpList

# show bar graph using matplotlib.pyplot
def ShowRevenueGraph(fYear, fObjList):
    fig, ax = plt.subplots()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    counts = GetGraphList(fYear, fObjList)
    bar_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
    bar_colors = [constants.CYAN, constants.RED, constants.GREEN, constants.ORANGE, constants.NAVY, constants.MAGENTA, constants.OLIVE, constants.YELLOW, constants.PURPLE, constants.GRAY, constants.BURGUNDY, constants.PINK]
    ax.bar(months, counts, label=bar_labels, color=bar_colors)
    ax.set_ylabel("Revenue (EUR)") 
    ax.set_title("Revenue " + str(fYear)) 
    plt.show()
    