import psycopg2, csv, random

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()

cursor.execute('''
        DROP TABLE IF EXISTS soortgelijke_producten;
        CREATE TABLE soortgelijke_producten(
            products_id varchar,
            products_ids varchar
        );
        ALTER TABLE soortgelijke_producten 
        ADD FOREIGN KEY (products_id) REFERENCES products(_id);

        ''')
connection.commit()

def get_all_products():
    products = {}
    query = '''
        SELECT _id, categories_id, brands_id FROM products'''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        products[row[0]] = {
            'category': row[1],
            'brand': row[2]
        }
    return products

get_all_products()

cursor.execute('''
        DROP TABLE IF EXISTS anderen_kochten_ook;  
        CREATE TABLE anderen_kochten_ook(
            products_id varchar,
            segment varchar,
            devicetype varchar
        );
        ALTER TABLE anderen_kochten_ook 
        ADD FOREIGN KEY (products_id) REFERENCES products(_id);
        ''')
