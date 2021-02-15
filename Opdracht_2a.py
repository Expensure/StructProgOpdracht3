from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://test:test@opisopshop.aalnc.mongodb.net/test?authSource=admin&replicaSet=atlas-lr7h7d-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
db = client.OpOpShop
prod_db = db.prod_small


def find_first_product():
    return prod_db.find_one()


def find_first_with_letter(string):
    cursor = prod_db.find({})
    for document in cursor:
        name = document["name"]
        if name.startswith(string) == True:
            break
    return document


def find_mean_price():
    totalprice = 0
    cursor = prod_db.find({})
    for document in cursor:
        totalprice += (int(document["price"]["selling_price"]/100))
    return totalprice / 1000

print('naam:',find_first_product()["name"],'|prijs:',find_first_product()["price"]["selling_price"]/100)
print('naam:',find_first_with_letter('R')["name"])
print(find_mean_price())
