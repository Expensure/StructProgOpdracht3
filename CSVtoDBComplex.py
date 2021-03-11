import psycopg2
import csv

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()


def writeCategories():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        list_of_combinations = []
        for row in reader:
            category_comb = [row[3],row[4],row[5]]
            if category_comb not in list_of_combinations:
                list_of_combinations.append(category_comb)
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            for i in list_of_combinations:
                if [row[3],row[4],row[5]] == i:
                    row.append(list_of_combinations.index(i))
            cursor.execute(
                """ 
                INSERT INTO categories (_id, category_1, category_2, category_3) 
                VALUES (%s,%s,%s,%s) ON CONFLICT (_id) DO NOTHING
                """,
                (row[7], row[3],row[4],row[5]))


def writeBrands():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        list_of_brands = []
        for row in reader:
            if row[6] not in list_of_brands:
                list_of_brands.append(row[6])
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            for i in list_of_brands:
                if row[6] == i:
                    row.append(list_of_brands.index(i))
            cursor.execute(
                """ 
                INSERT INTO brands (_id, brand) 
                VALUES (%s,%s) ON CONFLICT (_id) DO NOTHING
                """,
                (row[7], row[6]))


writeBrands()
writeCategories()
connection.commit()
cursor.close()
connection.close()
print("Data imported.")