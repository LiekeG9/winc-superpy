START_ID_BOUGHT = 1000
START_ID_SOLD = 5000

# Base class contains method for generating new ID
class BaseClass():
    def GetNewId(self, fId, fList):
        # find highest ID
        fNewId = fId
        for obj in fList:
            for key, value in obj.__dict__.items():
                if key == "id":
                    if int(value) > fNewId:
                        fNewId = int(value)
        # add 1 to highest value
        fNewId = fNewId + 1
        return fNewId

# Class for Bought rows (class is derived from Base class)
class Bought(BaseClass):
    def __init__(self, id, product_name, buy_date, buy_price, expiration_date, fListBought):
        if id == -1: # when creating a new row, generate ID
            self.id = super().GetNewId(START_ID_BOUGHT, fListBought)
        else: # when importing, use ID from imported file
            self.id = id
        self.product_name = product_name
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.expiration_date = expiration_date

# Class for Sold rows (class is derived from Base class)
class Sold(BaseClass):
    def __init__(self, id, bought_id, sell_date, sell_price, fListSold):
        if id == -1: # when creating a new row, generate ID
            self.id = super().GetNewId(START_ID_SOLD, fListSold)
        else: # when importing, use ID from imported file
            self.id = id
        self.bought_id = bought_id
        self.sell_date = sell_date
        self.sell_price = sell_price

# Class for Inventory rows
class Inventory:
    def __init__(self, product_name, count, buy_price, expiration_date):
        self.product_name = product_name
        self.count = count
        self.buy_price = buy_price
        self.expiration_date = expiration_date
