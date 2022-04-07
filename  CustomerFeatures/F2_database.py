import sqlite3


def create_table():
    with sqlite3.connect('./python_cw.db') as conn:
        cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "toys" (
                        "toy_id"	INTEGER NOT NULL UNIQUE,
                        "toy_category"	TEXT NOT NULL,
                        "toy_name"	TEXT NOT NULL,
                        "toy_image"	BLOB NOT NULL,
                        "toy_quantity"	INTEGER NOT NULL,
                        "toy_price"	REAL NOT NULL,
                        "toy_descrip"	TEXT NOT NULL,
                        PRIMARY KEY("toy_id" AUTOINCREMENT)
                        );""")
    conn.commit()
    cursor.close()
    conn.close()


def insert_data(toy_id, toy_category, toy_name, toy_quantity, toy_price, toy_descrip):
    """
    Inserts the data in table called 'toys'
    """
    try:
        with sqlite3.connect('./python_cw.db') as db:
            cursor = db.cursor()

        insert_query = """ INSERT INTO toys
                            (toy_id, toy_category, toy_name, toy_quantity, toy_price, toy_descrip)
                             VALUES (?, ?, ?, ?, ?, ?, ?)
                       """
        # Convert data into tuple format
        data_tuple = (toy_id, toy_category, toy_name, toy_quantity, toy_price, toy_descrip)
        cursor.execute(insert_query, data_tuple)
        db.commit()

    finally:
        cursor.close()
        db.close()

    # Inserting the data
    # insert_data(1, 'Board', 'Monopoly', "C:/Users/44744/Desktop/python/images/Monopoly.png", 30, 20, 'Amazing toy')


def fetch_category():
    """
    Fetch the data from the database
    """
    try:
        with sqlite3.connect('./python_cw.db') as db:
            cursor = db.cursor()

        select_query = 'SELECT DISTINCT toy_category FROM toys'
        cursor.execute(select_query)
        category = cursor.fetchall()
        return category

    finally:
        cursor.close()
        db.close()


def fetch_name(toy_category):
    """
    Fetch the toy_name from the database
    """
    try:
        with sqlite3.connect('./python_cw.db') as db:
            cursor = db.cursor()
            toy_name_query = 'SELECT toy_name FROM toys WHERE toy_category = ?'
            cursor.execute(toy_name_query, (toy_category,))
            name = cursor.fetchall()
            return name

    finally:
        cursor.close()
        db.close()


def fetch_price(toy_category):
    """
    Fetch the toy_price from the database
    """
    try:
        with sqlite3.connect('./python_cw.db') as db:
            cursor = db.cursor()
            toy_price_query = 'SELECT toy_price FROM toys WHERE toy_category = ?'
            cursor.execute(toy_price_query, (toy_category,))
            price = cursor.fetchall()
            return price

    finally:
        cursor.close()
        db.close()


def fetch_stock(toy_category):
    """
    Fetch the toy_stock from the database
    """
    try:
        with sqlite3.connect('./python_cw.db') as db:
            cursor = db.cursor()
            toy_stock_query = 'SELECT toy_stock FROM toys WHERE toy_category = ?'
            cursor.execute(toy_stock_query, (toy_category,))
            stock = cursor.fetchall()
            return stock

    finally:
        cursor.close()
        db.close()


def all_toys():
    """
    List of all toys
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT toy_name FROM toys'
            cursor.execute(query)
            data = cursor.fetchall()
            return data

    finally:
        cursor.close()
        db.close()


# ======================== TOY-SPECIFIC ================================

def toyprice(toy_name):
    """
    Fetch the toyprice BASED on search.get()
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT toy_price FROM toys WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            record = cursor.fetchall()
            return record

    finally:
        cursor.close()
        db.close()


def toystock(toy_name):
    """
    Fetch the toystock BASED on search.get()
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT toy_stock FROM toys WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            record = cursor.fetchall()
            return record

    finally:
        cursor.close()
        db.close()


def toydescrip(toy_name):
    """
    Fetch the toydesciption BASED on search.get()
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT toy_descrip FROM toys WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            record = cursor.fetchall()
            return record

    finally:
        cursor.close()
        db.close()


# ======================== LOW-STOCK or OUT OF STOCK ================================

def check_stock(toy_category):
    """
    For checking the stock status BASED on toy_category
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT case when toy_stock = 0 then "Out of Stock"' \
                    '       when toy_stock<20 then "Low Stock" ' \
                    '      else toy_stock end as st FROM toys ' \
                    'WHERE toy_category = ? '
            cursor.execute(query, (toy_category,))
            record = cursor.fetchall()
            return record

    finally:
        cursor.close()
        db.close()


# ======================== REVIEWS ================================

def createreview():
    """
    Create reviews table in the database
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS "reviews" (
                        "customer"  TEXT,
                        "toy_name"	TEXT,
                        "rating"  TEXT,
                        "review" TEXT,
                        "review_date" DATE
                        );""")
    finally:
        cursor.close()
        db.close()


def fetch_customer(toy_name):
    """
    Fetch the customer name
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT customer FROM reviews WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            data = cursor.fetchall()
            return data
    finally:
        cursor.close()
        db.close()


def fetch_rating(toy_name):
    """
    Rating submit by the customer
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT rating FROM reviews WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            rate = cursor.fetchall()
            return rate

    finally:
        cursor.close()
        db.close()


def fetch_review(toy_name):
    """
    Review submitted by the customer
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT review FROM reviews WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            data = cursor.fetchall()
            return data

    finally:
        cursor.close()
        db.close()


def fetch_date(toy_name):
    """
    Date when the review was submitted
    """
    try:
        with sqlite3.connect("./python_cw.db") as db:
            cursor = db.cursor()
            query = 'SELECT review_date FROM reviews WHERE toy_name = ?'
            cursor.execute(query, (toy_name,))
            date = cursor.fetchall()
            return date
    finally:
        cursor.close()
        db.close()
