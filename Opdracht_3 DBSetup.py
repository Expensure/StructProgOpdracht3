import psycopg2

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")

cur = connection.cursor()

cur.execute('''
        DROP TABLE IF EXISTS anderen_kochten_ook;
        DROP TABLE IF EXISTS soortgelijke_producten;
        CREATE TABLE anderen_kochten_ook(
            prodid varchar,
            segment varchar,
            devicetype varchar
        );
        CREATE TABLE soortgelijke_producten(
            prodid varchar,
            prodids varchar
        );
        ALTER TABLE anderen_kochten_ook 
        ADD FOREIGN KEY (prodid) REFERENCES products(_id);
        ALTER TABLE soortgelijke_producten
        ADD FOREIGN KEY (prodid) REFERENCES products(_id);

        ''')
connection.commit()
print("Added tables")