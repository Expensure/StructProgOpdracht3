import psycopg2, csv, ast, random

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()


def strlistreader(input):
    # Makes string-like lists actual lists
    return ast.literal_eval(input)


def create_table():
    # Creates table anderen_kochten_ook with profile and four products as recommendations
    cursor.execute('''
        DROP TABLE IF EXISTS anderen_kochten_ook;
        CREATE TABLE anderen_kochten_ook(
            profiles_id varchar,
            products_id1 varchar,
            products_id2 varchar,
            products_id3 varchar,
            products_id4 varchar
        );
        ''')
    connection.commit()
    return None


def get_products_per_user():
    '''
    Creates a better profiles_previously_viewed CSV so all products are within profile (like Primary key)
    :return: Nothing
    '''
    query = '''SELECT * FROM profiles_previously_viewed '''
    cursor.execute(query)
    rows = cursor.fetchall()
    user_products = {}
    users_used = []
    x = 0
    for row in rows:
        x += 1
        if row[0] not in users_used:
            users_used.append(row[0])
            user_products[row[0]] = [row[1]]
        else:
            user_products[row[0]].append(row[1])
        if x == 500000:  # Gelimiteerd omdat 1.7 miljoen entries kost exponentieel meer tijd.
            break
    with open('user_kocht.csv', 'w') as writable:
        names = ['profiles_id', 'products_ids']
        writer = csv.DictWriter(writable, fieldnames=names)
        writer.writeheader()
        for item in user_products:
            writer.writerow({'profiles_id': item, 'products_ids': user_products[item]})


def get_profiletype():
    '''
    Checks how many products every profile has watched, and classifies them.
    We can not use profiles in recommendations that only have the same product as user, so profiles with 1 view can not be used.
    Returns all profiles that have 5 products and all profiles that have 2-4 products
    '''
    with open('user_kocht.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        big_profiles = []
        other_profiles = []
        for row in reader:
            if len(row) == 2:
                if len(strlistreader(row[1])) > 4:
                    big_profiles.append(row[0])
                elif len(strlistreader(row[1])) > 1:
                    other_profiles.append(row[0])
            else:
                continue
    return big_profiles, other_profiles


def recomm(bows, row, big_profiles, low_profiles):
    '''
    :param bows: All rows, copy
    :param row: Current row to not recommend itself
    :param big_profiles: All profiles with 5 products watched
    :param low_profiles: All profiles with 2-4 products watched
    :return: Recommendation for row of 4 products based on comparison bows and row
    '''
    recommendation = []
    x = 0
    users_used = []
    for bow in bows:
        x += 1
        products_of_user = strlistreader(bow[1])
        if bow[0] != row[0]:
            for i in strlistreader(row[1]):
                if len(
                        recommendation) == 4 or x == 30000:  # If recommendations made or checked too many entries to find reliable recommendations
                    return recommendation

                if i in products_of_user:
                    if bow[
                        0] in big_profiles:  # If found user has 5 products viewed, recommendation = all products - equal product. Overwrites low_profile
                        users_used.append(bow[0])
                        products_of_user.remove(i)
                        recommendation = list(products_of_user)

                    elif bow[0] in low_profiles and bow[
                        0] not in users_used:  # If found user that has 2-4 products viewed: select a random product from
                        users_used.append(bow[0])
                        products_of_user.remove(i)
                        recommendation.append(random.choice(products_of_user))


def get_recommendation():
    '''
    Stable basis on creating recommendations
    fills (partly) unfilled recommendations with random products.
    :return: All recommendations per profile
    '''
    x = 0
    big_profiles, low_profiles = get_profiletype()
    print('got profiletypes')
    recommendation_per_profile = {}
    rows = []
    with open('user_kocht.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) == 2:
                rows.append(row)
        bows = rows.copy()
        for row in rows:
            x += 1
            recommendation = (recomm(bows, row, big_profiles, low_profiles))
            while len(recommendation) != 4:
                recommendation.append(random.choice(strlistreader((random.choice(rows))[1])))  # Unfilled recommendations filled with random products
            recommendation_per_profile[row[0]] = recommendation
            if x % 100 == 0:
                print(x, "Recommendations written")
            if x == 30000:
                print("Written 30000 recommendations now, will do for now")
                return recommendation_per_profile
    return recommendation_per_profile


def make_csv_others_bought(recommendations):
    print("Finishing up")
    # Make CSV file from data
    with open('anderen_kochten_ook.csv', 'w') as writable:
        names = ['profiles_id', 'products_id1', 'products_id2', 'products_id3', 'products_id4']
        writer = csv.DictWriter(writable, fieldnames=names)
        writer.writeheader()
        for item in recommendations:
            writer.writerow(
                {'profiles_id': item,
                 'products_id1': recommendations[item][0],
                 'products_id2': recommendations[item][1],
                 'products_id3': recommendations[item][2],
                 'products_id4': recommendations[item][3]}
            )
def to_db():
    #make_csv_others_bought(get_recommendation())
    with open('anderen_kochten_ook.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row != []:
                cursor.execute(
                """ 
                INSERT INTO anderen_kochten_ook (profiles_id,products_id1,products_id2,products_id3,products_id4) 
                VALUES (%s,%s,%s,%s,%s) """,
                (row[0], row[1], row[2], row[3], row[4]))
                connection.commit()

# bigs,smalls = get_profiletype()
create_table()
to_db()
connection.close()
print("All done!")