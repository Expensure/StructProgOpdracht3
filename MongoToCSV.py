from pymongo import MongoClient
import csv

client = MongoClient('mongodb+srv://test:test@opisopshop.aalnc.mongodb.net/test?authSource=admin&replicaSet=atlas-lr7h7d-shard-0'
    '&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
database = client.OpOpShop

products = database.products.find()
sessions = database.ses_small.find()
profiles = database.prof_small.find()

def multi_getattr(obj, attr, default = None):
    """
    http://code.activestate.com/recipes/577346-getattr-with-arbitrary-depth/
    Main Source
    Was slightly edited
    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = obj.get(i)
        except AttributeError:
            try:
                obj = obj[int(i)]
            except:
                return default
    return obj

def generateCSV(fileNameString, category, fieldnames, values):
    print("Creating the product database contents...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        c = 0
        for record in category:
            write_dict = {}
            for x in range(len(fieldnames)):
                if x == 0:
                    _id = multi_getattr(record,values[0],'')
                    if _id != '':
                        dash_index = str(_id).find('-')
                        if dash_index != -1:
                            write_dict.update({fieldnames[x]: _id[:dash_index] })
                        else:
                            try:
                                if fileNameString != 'sessions.csv':
                                    int(record[values[0]])
                                write_dict.update({fieldnames[x]: _id })
                            except:
                                pass
                    else:
                        write_dict.update({fieldnames[x]: c })
                else:
                    write_dict.update({fieldnames[x]: multi_getattr(record, values[x])})
                    x += 1
            writer.writerow(write_dict)
            c += 1
            if c % 10000 == 0:
                print("{} product records written...".format(c))
    print(f"Finished creating {fileNameString}")


generateCSV('products.csv', products,
            ['id', 'name', 'price', 'category', 'subcategory', 'subsubcategory', 'brand'],
            ["_id", "name", "price", "category", "sub_category", "sub_sub_category", "brand"])
generateCSV('sessions.csv', sessions,
            ['id', 'device', 'segment','orders'],
            ['buid.0', 'user_agent.device.model', 'segment','order.products'])
generateCSV('profiles.csv', profiles,
            ['_id','orders', 'buid'],
            ['_id', 'order.ids',"buids.0"])
