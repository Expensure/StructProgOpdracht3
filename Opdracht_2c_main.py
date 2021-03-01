# Connect to mongoDB:
from pymongo import MongoClient
import random
import psycopg2

client = MongoClient(
    'mongodb+srv://test:test@opisopshop.aalnc.mongodb.net/test?authSource=admin&replicaSet=atlas-lr7h7d-shard-0'
    '&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
# ^ Be sure to change this link when connecting your own client ^
db = client.OpOpShop
prod_db = db.prod_small

# Connect to database:
conn = psycopg2.connect(
    host="localhost",
    database="OpOpShop",
    user="postgres",
    password="postgres")
pg_cursor = conn.cursor


# TODO: Adding some product entries to PostgreSQL database:
def random_entries(amount=100):
    # Selects x amount of entries from all products, default = 100
    cursor = prod_db.find({})
    documentlist = []
    for document in cursor:
        documentlist.append(document)
    short_doc_list = []
    selection = ""
    for i in range(amount):
        while selection not in short_doc_list and selection == "":
            selection = random.choice(documentlist)
        short_doc_list.append(selection)
    return short_doc_list


def transfer_entries(lst):
    for i in lst:
        print(i)
        print(i['_id'])
        print(i['name'])
        sql = "INSERT INTO products (name,price) VALUES (%s,%s);"
        pg_cursor.execute(sql, (i['name'], i['price']['discount']))
        conn.commit()
    return None


transfer_entries(random_entries(100))

conn.close()
