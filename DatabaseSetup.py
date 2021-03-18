import psycopg2


""" Run this file to generate the whole database, you only need to personify the parameters of the postgresql database to acces your database """


connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()

cursor.execute(
            """DROP TABLE IF EXISTS brands CASCADE;
            CREATE  TABLE IF NOT EXISTS 
            brands 
            (_id varchar(255),
             brand varchar(255),
              PRIMARY KEY (_id))"""
)
cursor.execute(
            """DROP TABLE IF EXISTS categories CASCADE;
            CREATE  TABLE IF NOT EXISTS 
            categories
             (_id varchar(999),
              category_1 varchar(999),
               category_2 varchar(999),
                category_3 varchar(999),
                 PRIMARY KEY (_id));"""
)


cursor.execute(
            """DROP TABLE IF EXISTS products CASCADE;
                CREATE TABLE IF NOT EXISTS 
                products
                 (_id varchar(255),
                  categories_id varchar(255),
                   brands_id varchar(255),
                    price int4,
                     name varchar(255),
                         PRIMARY KEY (_id))"""
)

cursor.execute(
            """DROP TABLE IF EXISTS profiles CASCADE;
                CREATE TABLE IF NOT EXISTS profiles (
                    buids varchar(9999) ,
                    orders varchar(9999),
                    
            PRIMARY KEY (buids) );
"""
)
cursor.execute(
            """DROP TABLE IF EXISTS sessions CASCADE;
                CREATE TABLE IF NOT EXISTS
                 sessions
                  (_id varchar(255),
                    browser_id varchar(255),
                     profiles_id varchar(255),
                      segment varchar(255),
                       session_start timestamp,
                        session_end timestamp,
                         orders varchar(255),
                         PRIMARY KEY (_id));

"""
)
cursor.execute(
    """DROP TABLE IF EXISTS profiles_previously_viewed CASCADE;
        CREATE TABLE IF NOT EXISTS profiles_previously_viewed (
            profiles_id varchar(9999) ,
            products_ids varchar(9999));
"""
)


connection.commit()
cursor.close()
connection.close()
print("PostgreSQL datebase is (re)created")