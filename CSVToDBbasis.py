import psycopg2
import csv

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()

def writeProducts():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            print(row)
            cursor.execute("SELECT brands._id FROM brands WHERE brand = %s ", (row[4],))
            brand_id = cursor.fetchone()
            cursor.execute("SELECT categories._id FROM categories ")
            category_id = cursor.fetchone()
            print(brand_id)
            cursor.execute(
                """ 
                INSERT INTO products (id,name,gender,category_id,brand_id) 
                VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING
                """,
                (row[0], row[1], row[2], category_id[0], brand_id[0]))
def writeSessions():
    with open('sessions.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            sql = """INSERT INTO sessions (_id, browser_id,segment,orders) VALUES (%s, %s,%s,%s)"""
            cursor.execute(sql, (row[0], row[1], row[2]))


def writeProfiles():
    with open('profiles.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            sql = """INSERT INTO profiles (_id,order_amount,browser_id) VALUES (%s,%s,%s)"""
            cursor.execute(sql, (row[0], row[1], row[2]))

writeProducts()
writeSessions()
writeProfiles()
connection.commit()
cursor.close()
connection.close()
print("Data imported.")


