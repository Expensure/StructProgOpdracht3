import psycopg2, csv, random

connection = psycopg2.connect(user="postgres",
                              password="postgres",
                              host="localhost",
                              port="5432",
                              database="OpOpShop")
cursor = connection.cursor()
def create_soortgelijke_producten():
    cursor.execute('''
        DROP TABLE IF EXISTS soortgelijke_producten;
        CREATE TABLE soortgelijke_producten(
            products_id varchar,
            products_id1 varchar,
            products_id2 varchar,
            products_id3 varchar,
            products_id4 varchar,
            products_id5 varchar
        );
        ALTER TABLE soortgelijke_producten 
        ADD FOREIGN KEY (products_id) REFERENCES products(_id);

        ''')
    connection.commit()
    return None

def get_all_products():
    create_soortgelijke_producten()
    products = {}
    categories = {}
    total = {}
    query1 = '''SELECT _id, categories_id, brands_id FROM products'''
    cursor.execute(query1)
    rows1 = cursor.fetchall()
    for row in rows1:
        products[row[0]] = {
            'category_id': row[1],
            'brand': row[2]
        }
    query2 = '''SELECT * FROM categories'''
    cursor.execute(query2)
    rows2 = cursor.fetchall()
    for row in rows2:
        categories[row[0]] = {
            'category': row[1],
            'subcategory': row[2],
            'subsubcategory': row[3]
        }

    # Get all categories into the main query so we can distinguish category and subcategories.
    for row in rows1:
        for i, j in categories.items():
            if str(i[0]) == str(row[1]):
                total[row[0]] = {
                    'category': j.get('category'),
                    'subcategory': j.get('subcategory'),
                    'subsubcategory': j.get('subsubcategory'),
                    'brand': row[2]
                }
    return total

def get_recommendations_products(products):
    recommendation = {}
    for prod_index, prod_items in products.items():
        category = prod_items.get('category')
        subcategory = prod_items.get('subcategory')
        subsubcategory = prod_items.get('subsubcategory')
        brand = prod_items.get('brand')
        recommendations_category = []
        recommendations_subcategory = []
        recommendations_subsubcategory = []
        recommendations_brand = []
        for recom_index, recom_items in products.items():
            if recom_index != prod_index:
                if recom_items.get('category') == category:
                    recommendations_category.append(recom_index)
                    if recom_items.get('subcategory') == subcategory:
                        recommendations_subcategory.append(recom_index)
                        if recom_items.get('subsubcategory') == subsubcategory:
                            recommendations_subsubcategory.append(recom_index)
                            if recom_items.get('brand') == brand:
                                recommendations_brand.append(recom_index)
        if len(recommendations_subsubcategory) >= 5:
            recommended = random.sample(recommendations_subsubcategory, 5)
        elif len(recommendations_brand) >= 5:
            recommended = random.sample(recommendations_brand, 5)
        elif len(recommendations_subcategory) >= 5:
            recommended = random.sample(recommendations_subcategory, 5)
        elif len(recommendations_category) >= 5:
            recommended = random.sample(recommendations_category, 5)
        else:
            recommended = random.sample(list(products.keys()), 5)
        recommendation[prod_index] = recommended
    return recommendation

def make_csv_prod_recs(recommendations):
    with open('soortgelijkeproducten.csv', 'w') as writable:
        names = ['products_id', 'products_id1', 'products_id2', 'products_id3', 'products_id4', 'products_id5']
        writer = csv.DictWriter(writable, fieldnames= names)
        writer.writeheader()
        for item in recommendations:
            writer.writerow(
                {'products_id': item,
                 'products_id1': recommendations[item][0],
                 'products_id2': recommendations[item][1],
                 'products_id3': recommendations[item][2],
                 'products_id4': recommendations[item][3],
                 'products_id5': recommendations[item][4]}
            )

def producten_to_db():
    make_csv_prod_recs(get_recommendations_products(get_all_products()))
    with open('soortgelijkeproducten.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row != []:
                cursor.execute(
                """ 
                INSERT INTO soortgelijke_producten (products_id,products_id1,products_id2,products_id3,products_id4,products_id5) 
                VALUES (%s,%s,%s,%s,%s,%s) """,
                (row[0], row[1], row[2], row[3], row[4], row[5]))
                connection.commit()

producten_to_db()
print('Soortgelijke producten filled')
