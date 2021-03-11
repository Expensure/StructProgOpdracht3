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
        list_of_brands = []
        for row in reader:
            if row[6] not in list_of_brands:
                list_of_brands.append(row[6])

        for row
        for i in list_of_brands:
            for i in row:

        print(len(list_of_brands))
        for
        for i in list_of_brands:
            row.append(list_of_brands.index(i))
            print(row)
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
writeBrands()
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