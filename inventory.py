import classes
import datetime

# make inventory objects for all unsold products, from perspective of given date
def calculate_inventory_list(fDate, fListBought, fListSold, fListInventory):
    fListInventory.clear()
    for obj_bought in fListBought:
        # kijk alleen naar producten die voor/op peildatum zijn ingekocht        
        if obj_bought.buy_date <= datetime.datetime.strftime(fDate, "%Y-%m-%d"):
            # controleer of product nog NIET is verkocht voor/op peildatum
            tmpSold = False
            for obj_sold in fListSold:
                if (obj_sold.bought_id == obj_bought.id) and \
                    (obj_sold.sell_date <= datetime.datetime.strftime(fDate, "%Y-%m-%d")):
                    tmpSold = True
            # indien product nog NIET verkocht dan toevoegen op voorraadlijst
            if tmpSold == False: 
                # indien zelfde artikel (zelfde naam, prijs, exp.datum) al voorkomt, dan alleen aantal ophogen bestaande regel    
                tmpAdded = False
                for obj_inventory in fListInventory:
                    if (obj_bought.product_name.lower() == obj_inventory.product_name.lower()) and \
                        (obj_bought.buy_price == obj_inventory.buy_price) and \
                        (obj_bought.expiration_date == obj_inventory.expiration_date):
                        obj_inventory.count = obj_inventory.count + 1
                        tmpAdded = True
                # indien nog geen aantal is verhoogd dan moet er een nieuwe voorraadregel worden aangemaakt
                if tmpAdded == False:
                    fListInventory.append(classes.Inventory(obj_bought.product_name, 1, obj_bought.buy_price, obj_bought.expiration_date))
