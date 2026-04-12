import pymysql
from pymysql import MySQLError


def db_connect():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='pizzeria_pm02',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    except MySQLError as e:
        print('Ошибка подключения', e)
        return None


# ---------- авторизация ----------

def check_login(username, password):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    users.user_id AS id,
    users.full_name,
    roles.role_name AS role
FROM users
JOIN roles ON roles.role_id = users.role_id
WHERE users.username = %s AND users.password = %s
""", (username, password))
            return cursor.fetchone()
    finally:
        db.close()


# ---------- меню ----------

def all_menu_items():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    menu_items.item_id,
    menu_items.name,
    menu_items.description,
    menu_items.price,
    menu_items.category,
    menu_items.image,
    menu_items.offer_id,
    special_offers.discount_percentage,
    special_offers.name AS offer_name
FROM menu_items
LEFT JOIN special_offers 
	ON special_offers.offer_id = menu_items.offer_id
   AND CURDATE() BETWEEN special_offers.valid_from AND special_offers.valid_to
ORDER BY menu_items.item_id
""")
            return cursor.fetchall()
    finally:
        db.close()

def one_menu_item(item_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    menu_items.item_id,
    menu_items.name,
    menu_items.description,
    menu_items.price,
    menu_items.category,
    menu_items.image,
    menu_items.offer_id,
    special_offers.discount_percentage,
    special_offers.name AS offer_name
FROM menu_items
LEFT JOIN special_offers 
	ON special_offers.offer_id = menu_items.offer_id
   AND CURDATE() BETWEEN special_offers.valid_from AND special_offers.valid_to
WHERE menu_items.item_id = %s
""",(item_id,))
            return cursor.fetchone()
    finally:
        db.close()


def all_categories():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT DISTINCT category
FROM menu_items
ORDER BY category
""")
            rows = cursor.fetchall()
            return [row['category'] for row in rows]
    finally:
        db.close()


def add_menu_item(name, description, price, category, image, offer_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO menu_items (name, description, price, category, image, offer_id)
VALUES (%s, %s, %s, %s, %s, %s)
""", (name, description, price, category, image or None, offer_id))
            return True
    except Exception as e:
        print('Ошибка добавления позиции меню', e)
        return False
    finally:
        db.close()


def edit_menu_item(item_id, name, description, price, category, image, offer_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
UPDATE menu_items
SET name = %s, description = %s, price = %s, category = %s, image = %s, offer_id = %s
WHERE item_id = %s
""", (name, description, price, category, image or None, offer_id, item_id))
            return True
    except Exception as e:
        print('Ошибка изменения позиции меню', e)
        return False
    finally:
        db.close()


def delete_menu_item(item_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
            return True
    except Exception as e:
        print('Ошибка удаления позиции меню', e)
        return False
    finally:
        db.close()


# ---------- акции ----------

def all_offers():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    offer_id AS id,
    name,
    description,
    discount_percentage,
    valid_from,
    valid_to
FROM special_offers
ORDER BY offer_id
""")
            return cursor.fetchall()
    finally:
        db.close()


def one_offer(offer_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    offer_id AS id,
    name,
    description,
    discount_percentage,
    valid_from,
    valid_to
FROM special_offers
WHERE offer_id = %s
""", (offer_id,))
            return cursor.fetchone()
    finally:
        db.close()


def add_offer(name, description, discount_percentage, valid_from, valid_to):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO special_offers (name, description, discount_percentage, valid_from, valid_to)
VALUES (%s, %s, %s, %s, %s)
""", (name, description, discount_percentage, valid_from, valid_to))
            return True
    except Exception as e:
        print('Ошибка добавления акции', e)
        return False
    finally:
        db.close()


def edit_offer(offer_id, name, description, discount_percentage, valid_from, valid_to):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
UPDATE special_offers
SET name = %s, description = %s, discount_percentage = %s, valid_from = %s, valid_to = %s
WHERE offer_id = %s
""", (name, description, discount_percentage, valid_from, valid_to, offer_id))
            return True
    except Exception as e:
        print('Ошибка изменения акции', e)
        return False
    finally:
        db.close()


def delete_offer(offer_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE menu_items SET offer_id = NULL WHERE offer_id = %s", (offer_id,))
            cursor.execute("DELETE FROM special_offers WHERE offer_id = %s", (offer_id,))
            return True
    except Exception as e:
        print('Ошибка удаления акции', e)
        return False
    finally:
        db.close()


# ---------- пользователи ----------

def all_users():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    users.user_id AS id,
    users.username,
    users.password,
    users.full_name,
    users.contact_info,
    users.role_id,
    roles.role_name AS role
FROM users
JOIN roles ON roles.role_id = users.role_id
ORDER BY users.user_id
""")
            return cursor.fetchall()
    finally:
        db.close()


def one_user(user_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    users.user_id AS id,
    users.username,
    users.password,
    users.full_name,
    users.contact_info,
    users.role_id,
    roles.role_name AS role
FROM users
JOIN roles ON roles.role_id = users.role_id
WHERE users.user_id = %s
""", (user_id,))
            return cursor.fetchone()
    finally:
        db.close()


def add_user(username, password, full_name, contact_info, role_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO users (username, password, full_name, contact_info, role_id)
VALUES (%s, %s, %s, %s, %s)
""", (username, password, full_name, contact_info or None, role_id))
            return True
    except Exception as e:
        print('Ошибка добавления пользователя', e)
        return False
    finally:
        db.close()


def edit_user(user_id, username, password, full_name, contact_info, role_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
UPDATE users
SET username = %s, password = %s, full_name = %s, contact_info = %s, role_id = %s
WHERE user_id = %s
""", (username, password, full_name, contact_info or None, role_id, user_id))
            return True
    except Exception as e:
        print('Ошибка изменения пользователя', e)
        return False
    finally:
        db.close()


def delete_user(user_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            return True
    except Exception as e:
        print('Ошибка удаления пользователя', e)
        return False
    finally:
        db.close()


# ---------- роли ----------

def all_roles():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT role_id AS id, role_name FROM roles ORDER BY role_id")
            return cursor.fetchall()
    finally:
        db.close()


def add_role(role_name):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO roles (role_name) VALUES (%s)", (role_name,))
            return True
    except Exception as e:
        print('Ошибка добавления роли', e)
        return False
    finally:
        db.close()


def edit_role(role_id, role_name):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE roles SET role_name = %s WHERE role_id = %s", (role_name, role_id))
            return True
    except Exception as e:
        print('Ошибка изменения роли', e)
        return False
    finally:
        db.close()


def delete_role(role_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
            return True
    except Exception as e:
        print('Ошибка удаления роли', e)
        return False
    finally:
        db.close()


# ---------- заказы ----------

def all_orders():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    orders.order_id,
    orders.user_id,
    users.full_name,
    orders.order_date,
    orders.order_type,
    orders.delivery_address,
    orders.customer_comment,
    orders.total_amount,
    orders.status
FROM orders
JOIN users ON users.user_id = orders.user_id
ORDER BY orders.order_id DESC
""")
            return cursor.fetchall()
    finally:
        db.close()


def filter_orders_status(status):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    orders.order_id,
    orders.user_id,
    users.full_name,
    orders.order_date,
    orders.order_type,
    orders.delivery_address,
    orders.customer_comment,
    orders.total_amount,
    orders.status
FROM orders
JOIN users ON users.user_id = orders.user_id
WHERE orders.status = %s
ORDER BY orders.order_id DESC
""", (status,))
            return cursor.fetchall()
    finally:
        db.close()


def orders_by_user(user_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    order_id,
    order_date,
    order_type,
    delivery_address,
    customer_comment,
    total_amount,
    status
FROM orders
WHERE user_id = %s
ORDER BY order_id DESC
""", (user_id,))
            return cursor.fetchall()
    finally:
        db.close()


def one_order(order_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    order_id,
    user_id,
    order_date,
    order_type,
    delivery_address,
    customer_comment,
    total_amount,
    status
FROM orders
WHERE order_id = %s
""", (order_id,))
            return cursor.fetchone()
    finally:
        db.close()


def add_order(user_id, order_type, delivery_address, customer_comment, total_amount, status='Ожидает приготовления'):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO orders (user_id, order_type, delivery_address, customer_comment, total_amount, status)
VALUES (%s, %s, %s, %s, %s, %s)
""", (user_id, order_type, delivery_address or None, customer_comment or None, total_amount, status))
            return cursor.lastrowid
    except Exception as e:
        print('Ошибка добавления заказа', e)
        return None
    finally:
        db.close()


def add_order_item(order_id, item_id, quantity, unit_price):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO order_items (order_id, item_id, quantity, unit_price)
VALUES (%s, %s, %s, %s)
""", (order_id, item_id, quantity, unit_price))
            return True
    except Exception as e:
        print('Ошибка добавления позиции заказа', e)
        return False
    finally:
        db.close()


def edit_order(order_id, order_type, delivery_address, customer_comment, total_amount, status):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
UPDATE orders
SET order_type = %s, delivery_address = %s, customer_comment = %s, total_amount = %s, status = %s
WHERE order_id = %s
""", (order_type, delivery_address or None, customer_comment or None, total_amount, status, order_id))
            return True
    except Exception as e:
        print('Ошибка изменения заказа', e)
        return False
    finally:
        db.close()


def delete_order(order_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
            return True
    except Exception as e:
        print('Ошибка удаления заказа', e)
        return False
    finally:
        db.close()


def update_order_status(order_id, status):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id))
            return True
    except Exception as e:
        print('Ошибка изменения статуса заказа', e)
        return False
    finally:
        db.close()


# ---------- отзывы ----------

def reviews_by_user(user_id):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    reviews.review_id,
    menu_items.name AS item_name,
    reviews.rating,
    reviews.comment,
    reviews.review_date,
    reviews.item_id
FROM reviews
JOIN menu_items ON menu_items.item_id = reviews.item_id
WHERE reviews.user_id = %s
ORDER BY reviews.review_id DESC
""", (user_id,))
            return cursor.fetchall()
    finally:
        db.close()


def add_review(user_id, item_id, rating, comment):
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
INSERT INTO reviews (user_id, item_id, rating, comment)
VALUES (%s, %s, %s, %s)
""", (user_id, item_id, rating, comment))
            return True
    except Exception as e:
        print('Ошибка добавления отзыва', e)
        return False
    finally:
        db.close()


# ---------- аналитика ----------

def total_orders_sum():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT IFNULL(SUM(total_amount), 0) AS total_sum FROM orders")
            row = cursor.fetchone()
            return row or {'total_sum': 0}
    finally:
        db.close()


def orders_status_stats():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT status, COUNT(*) AS total_count
FROM orders
GROUP BY status
ORDER BY total_count DESC, status
""")
            return cursor.fetchall()
    finally:
        db.close()


def popular_items():
    db = db_connect()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
SELECT
    menu_items.name,
    SUM(order_items.quantity) AS total_quantity,
    SUM(order_items.quantity * order_items.unit_price) AS total_amount
FROM order_items
JOIN menu_items ON menu_items.item_id = order_items.item_id
GROUP BY menu_items.item_id, menu_items.name
ORDER BY total_quantity DESC, total_amount DESC
""")
            return cursor.fetchall()
    finally:
        db.close()
