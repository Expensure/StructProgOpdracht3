import psycopg2
import csv

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()

def writeBrandsAndProducts():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO brands(brand)
                SELECT %s WHERE NOT EXISTS (
                    SELECT 1 FROM brands WHERE brand=%s
                );""", (row[6], row[6]))

            cursor.execute("SELECT id FROM brands WHERE brand = %s ", (row[6],))
            brand_id = cursor.fetchone()

            cursor.execute(
                """ 
                INSERT INTO products (id,name,gender,category,subcategory,subsubcategory,brand_id) 
                VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING
                """,
                (row[0], row[1], row[2], row[3], row[4], row[5], brand_id[0]))


def writeSessions():
    with open('sessions.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            sql = """INSERT INTO sessions (browser_id,segment,orders) VALUES (%s,%s,%s)"""
            cursor.execute(sql, (row[0], row[1], row[2]))


def writeProfiles():
    with open('profiles.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            sql = """INSERT INTO profiles (id,order_amount,browser_id) VALUES (%s,%s,%s)"""
            cursor.execute(sql, (row[0], row[1], row[2]))

writeBrandsAndProducts()
writeProfiles()

connection.commit()
cursor.close()
connection.close()
print("Data imported.")