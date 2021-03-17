import psycopg2, csv, random

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()

def create_table():
    cursor.execute('''
        DROP TABLE IF EXISTS anderen_kochten_ook;  
        CREATE TABLE anderen_kochten_ook(
            profiles_id varchar,
            segment varchar,
            devicetype varchar,
            products_id1 varchar,
            products_id2 varchar,
            products_id3 varchar,
            products_id4 varchar,
            products_id5 varchar
        );
        ALTER TABLE anderen_kochten_ook 
        ADD FOREIGN KEY (profiles_id) REFERENCES profiles(_id);
        ''')
    connection.commit()
    return None

create_table()
connection.close()