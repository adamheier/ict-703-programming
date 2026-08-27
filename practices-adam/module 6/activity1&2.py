###Activity 1

inventory = {"Bolts":2, "Nails":17, "Screws": 5}

'''1. Print out a list of the products we have 
2. Add 5 new items to our inventory with the appropriate quantities (you choose the 5) 
3. Write a program to ask for the item and amount and add this to the inventory. 
4. Print out a list of the products we have and the amounts. Make sure the printout looks nice. 
5. Write a program that answers customer questions about how much stock we have on hand for a particular item. 
6. Write a program that allows a customer to buy items. When they choose an item and an amount, update the inventory to the new values 
7. Is a dictionary the best data structure for this application? What are the pros/cons of this data type for this application?'''

#1.
print("We currently have:", inventory)

#2
inventory["Hammer"] = 1
inventory["Saw"] = 3
inventory["Screwdriver"] = 7
inventory["Paint"] = 13
inventory["Brush"] = 4

#3
item = str(input("Please enter the item you would like to add to the inventory: "))
amount = int(input("Please enter the amount of this item you would like to add: "))
inventory[item] = amount

#4
print("We currently have the following items in our inventory:")
for item, amount in inventory.items():
    print(f"{item}: {amount}")

#5
question = str(input("Please enter the item you would like to check the quantity of: "))
if question in inventory:
    print(f"The quantity of {question} is: {inventory[question]}")
else: 
    print("Item not found in inventory.")

#6
purchase_item = str(input("Please enter the item you would like to purchase: "))
purchase_quantity = int(input("Please enter the quantity you would like to purchase: "))
if purchase_item in inventory:
    if inventory[purchase_item] >= purchase_quantity:
        inventory[purchase_item] -= purchase_quantity
        print(f"Purchase successful! {purchase_quantity} {purchase_item}(s) purchased.")
    else:
        print("Sorry, we don't have enough stock for that purchase.")
else: 
    print("Sorry we don't have this item in stock and you can't buy it, fuck off")


###Activity 2
'''Extension of the dict to store more information about the items.
Unique Stock code (eg "MA-1234”) 
Stock on hand (eg 10) 
Price (eg 12.50) 
Current Supplier (eg “East West Supplies”) 
Low stock warning amount (eg 3)

1. What data structure (s) are you going to use and why? 
2. Write a program that asks the store person to enter products and their details until they enter the product “Stop” 
3. Extend the program to ask a customer what they want to buy and quantity and then updates the inventory and prints out an invoice for the customer (single line with product, amount, price and total owing) 
4. Extend the program to print out a warning message to the store person if the stock is equal or below the low stock warning and who to order more from.'''



#1
'''object oriented
Andrew's version: Jeder Inhalt von davor z.B. Screws hat sein eigenes dict oder einfach eien Liste
pprint für besseres übersichtlichers print der Daten'''

#2
class Item:
    def __init__(self, name, stock_on_hand):
        self.name = name
        self.stock_on_hand = stock_on_hand
        self.unique_stock_code = input(f"Unique Stock Code for {name}: ")
        self.price = float(input(f"Price for {name}: ".replace(",", ".")))
        self.current_supplier = input(f"Current Supplier for {name}: ")
        self.low_stock_warning_amount = int(input(f"Low Stock Warning Amount for {name}: "))


#3
products = {}

# Bestehende Items aus Aufgabe 1 übernehmen und um die zusätzlichen Felder ergänzen
for name, quantity in inventory.items():
    products[name] = Item(name, quantity)

# Neue Produkte erfassen, bis "Stop" eingegeben wird
while True:
    name = input("Please enter the product name (or 'Stop' to finish): ")
    if name == "Stop":
        break
    quantity = int(input(f"Stock on Hand for {name}: "))
    products[name] = Item(name, quantity)

print("\nProducts entered:")
for name, product in products.items():
    print(f"{name}: stock={product.stock_on_hand}, price={product.price}")

#4
purchase_name = input("Please enter the product you would like to purchase: ")
if purchase_name in products:
    purchase_amount = int(input(f"Please enter the amount of {purchase_name} you would like to purchase: "))
    product = products[purchase_name]
    if product.stock_on_hand >= purchase_amount:
        product.stock_on_hand -= purchase_amount
        total = product.price * purchase_amount
        print(f"Invoice: {purchase_name} x{purchase_amount} @ {product.price:.2f} = {total:.2f}")

        if product.stock_on_hand <= product.low_stock_warning_amount:
            print(f"WARNING: Stock of {purchase_name} is low ({product.stock_on_hand} left). "
                  f"Please order more from {product.current_supplier}.")
    else:
        print("Sorry, we don't have enough stock for that purchase.")
else:
    print("Sorry, we don't have this product in stock.")

