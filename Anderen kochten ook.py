import psycopg2, csv, ast

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()


def strlistreader(input):
    return ast.literal_eval(input)


def create_table():
    cursor.execute('''
        DROP TABLE IF EXISTS anderen_kochten_ook;
        CREATE TABLE anderen_kochten_ook(
            profiles_id varchar,
            segment varchar,
            devicetype varchar
        );
        ALTER TABLE anderen_kochten_ook 
        ADD FOREIGN KEY (profiles_id) REFERENCES profiles(_id);
        ''')
    connection.commit()
    return None


def get_sessioninformation():
    def get_segments():
        segments = []
        seg_query = '''
                SELECT segment FROM sessions 
                GROUP BY segment'''
        cursor.execute(seg_query)
        rows = cursor.fetchall()
        for row in rows:
            row = row[0]
            if row != 'segment':
                segments.append(row)
        return segments

    def get_devices():
        devices = []
        dev_query = '''
                SELECT browser_id FROM sessions
                GROUP BY browser_id'''
        cursor.execute(dev_query)
        rows = cursor.fetchall()
        for row in rows:
            row = row[0]
            if row != 'device' and row != '':
                devices.append(row)
        return devices

    def get_combinations(listx, listy):
        combinations = []
        for x in listx:
            for y in listy:
                combinations.append(x + ":" + y)
        return combinations

    create_table()
    segs = get_segments()
    devs = get_devices()
    combos = get_combinations(segs, devs)
    return combos


def get_products_viewed():
    query = '''SELECT * FROM profiles_previously_viewed '''
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        
        print(row)


get_products_viewed()

connection.close()
