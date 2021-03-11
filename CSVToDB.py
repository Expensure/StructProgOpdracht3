import psycopg2
import csv

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()
def writeBrands():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            cursor.execute(
                """ 
                INSERT INTO brands (brand) 
                VALUES (%s) ON CONFLICT (brand) DO NOTHING
                """,
                (row[0]))
def writeProducts():
    with open('products.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute(
                """ 
                INSERT INTO products (_id,name) 
                VALUES (%s,%s) ON CONFLICT (_id) DO NOTHING
                """,
                (row[0], row[1]))

writeProducts()
connection.commit()
cursor.close()
connection.close()
print("Data imported.")




#def writeSessions():
    #with open('sessions.csv', 'r', encoding='utf8') as f:
        #reader = csv.reader(f)
        #for row in reader:
            #print(row)
            #sql = """INSERT INTO sessions (browser_id,segment,orders) VALUES (%s,%s,%s)"""
            #cursor.execute(sql, (row[0], row[1], row[2]))


#def writeProfiles():
    #with open('profiles.csv', 'r', encoding='utf8') as f:
        #reader = csv.reader(f)
        #for row in reader:
            #print(row)
            #sql = """INSERT INTO profiles (id,order_amount,browser_id) VALUES (%s,%s,%s)"""
            #cursor.execute(sql, (row[0], row[1], row[2]))


#writeSessions()
#writeProfiles()