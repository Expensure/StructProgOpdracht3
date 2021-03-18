import psycopg2, csv, ast, random

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
    recommendations_per_user = []
    for row in rows:
        users = []
        for bow in rows:
            if len(row) == 2 and len(bow) == 2:
                if row[1] != '' and bow[1] != '':
                    if row[0] != bow[0]:
                        if row[1] == bow[1]:
                            if bow[0] not in users:
                                users.append(bow[0])
        recommendations = []
        try:
            ranselect_user = random.sample(users, 5)
        except:
            cursor.execute("SELECT products_ids FROM profiles_previously_viewed")
            rows = cursor.fetchall()
            recommendations.append(random.sample(rows, 5))
            recommendations_per_user.append([row[0], random.sample(rows, 5)])
            break

        for i in ranselect_user:
            cursor.execute("SELECT products_ids FROM profiles_previously_viewed WHERE profiles_id = %(value)s """,
                           {"value": i})
            cows = cursor.fetchall()
            recommendations.append(list(random.choice(cows)))
            print(recommendations)
        recommendations_per_user.append([row[0], recommendations])
        print(recommendations_per_user)
    return recommendations_per_user


def make_csv(recommendations):
    with open('anderen_kochten_ook.csv', 'w') as writable:
        names = ['profiles_id', 'products_id1', 'products_id2', 'products_id3', 'products_id4', 'products_id5']
        writer = csv.DictWriter(writable, fieldnames=names)
        writer.writeheader()
        for item in recommendations:
            writer.writerow(
                {'profiles_id': item,
                 'products_id1': recommendations[item][0],
                 'products_id2': recommendations[item][1],
                 'products_id3': recommendations[item][2],
                 'products_id4': recommendations[item][3],
                 'products_id5': recommendations[item][4]}
            )

make_csv(get_products_viewed())

connection.close()
