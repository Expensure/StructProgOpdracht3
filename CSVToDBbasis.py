import psycopg2
import csv
import ast

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()


def writeProductsBrandsCategories():
    def row3reader(input):
        dicto = ast.literal_eval(input[3])
        newlist = list(dicto.values())
        if len(newlist) == 1:
            newlist.append('')
        if len(newlist) == 2:
            newlist.append('')
        return newlist

    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        list_of_combinations = []
        list_of_brands = []
        for row in reader:
            if row[6] not in list_of_brands:
                list_of_brands.append(row[6])
            category_comb = row3reader(row)
            if category_comb not in list_of_combinations:
                list_of_combinations.append(category_comb)
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            #Price
            priceinalist = (list((ast.literal_eval(row[2])).values()))
            price = priceinalist[0]/100
            #Brands
            for i in list_of_brands:
                if row[6] == i:
                    brand_id = (str(list_of_brands.index(i)))
            #Categories
            checkme = row3reader(row)
            for i in list_of_combinations:
                if checkme == i:
                    categorie_id = str(list_of_combinations.index(i))
            categorie, subcategorie, subsubcategorie = checkme[0], checkme[1], checkme[2]
            cursor.execute(
                """ 
                INSERT INTO products (_id,name,price,categories_id,brands_id) 
                VALUES (%s,%s,%s,%s,%s) ON CONFLICT (_id) DO NOTHING""",
                (row[0], row[1], price, brand_id, categorie_id))
            cursor.execute(
                """ 
                INSERT INTO brands (_id,brand) 
                VALUES (%s,%s) ON CONFLICT (_id) DO NOTHING""",
                (brand_id, row[6]))
            cursor.execute(
                """
                INSERT INTO categories (_id, category_1, category_2, category_3)
                VALUES (%s,%s,%s,%s) ON CONFLICT (_id) DO NOTHING
                 """,
                (categorie_id, categorie, subcategorie, subsubcategorie))


def writeSessions():
    with open('sessions.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute(
                """INSERT INTO sessions (_id, browser_id,segment,orders)
                 VALUES (%s,%s,%s,%s)  ON CONFLICT(_id) DO NOTHING""",
                (row[0], row[1], row[2], row[3]))


def writeProfiles():
    with open('profiles.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute(
                """INSERT INTO profiles (_id,order_amount)
                 VALUES (%s,%s) ON CONFLICT(_id) DO NOTHING""", (
                    row[0], row[1]))


writeProductsBrandsCategories()
writeSessions()
writeProfiles()
connection.commit()
cursor.close()
connection.close()
print("Data imported.")
