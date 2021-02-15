from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://test:test@opisopshop.aalnc.mongodb.net/test?authSource=admin&replicaSet=atlas-lr7h7d-shard-0'
    '&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
# ^ Be sure to change this when connecting your own client ^

db = client.OpOpShop
# Edit 'OpOpShop' to your own database name when adding your own MongoClient
prod_db = db.prod_small


# Edit 'prod_small' to your own collection name when adding your own MongoClient
# Here the collection is called prod_small because the writer uses both a sample collection and the entire one.


def find_first_product():
    # Finds first product in the collection
    return prod_db.find_one()
    # Note: find_one() always finds the first one that fits the query, There's no query, so no problem.


def find_first_with_letter(string):
    # Finds first product in the collection starting with the string it was given
    cursor = prod_db.find({})
    for document in cursor:
        name = document["name"]
        if name.startswith(string):
            # Breaks for loop because 'name starting with given string' has been found.
            break
    return document


def find_mean_price():
    # Goes through all entries of collection to get mean of all prices.
    totalprice = 0
    cursor = prod_db.find({})
    for document in cursor:
        totalprice += (int(document["price"]["selling_price"] / 100))
    return totalprice / 1000


print('naam:', find_first_product()["name"], '|prijs:', find_first_product()["price"]["selling_price"] / 100)
print('naam:', find_first_with_letter('R')["name"])
print(find_mean_price())
