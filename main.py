import re
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from pymysql import cursors
# import sqlalchemy


app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' # to be changed! (Used for debugging purposes)
app.config['MYSQL_DATABASE_DB'] = 'api_store'
mysql = MySQL(app)
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/api')
def index():
    return 'API for listing customers<BR>Usage:<BR>parameters: first_name, last_name, email, id<BR>/api/customers [GET/POST]<BR>/api/customers/&lt;id&gt; [GET/DELETE]<BR>/api/customers/update/&lt;id&gt; [UPDATE]', 200

@app.route('/api/customers', methods=['GET'])
def get_all_customers():
    customer_list = []
    try:
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        for row in customers:
            customer_list.append({'id': row[3], 'first_name': row[0], 'last_name': row[1], 'email': row[2]})
        return jsonify(customer_list)
    except Exception as e:
        print (e)
        return "No customers in database"

@app.route('/api/customers/<int:id>', methods=['GET'])
def get_one_customer(id):
    customer = []
    try:
        cursor.execute('SELECT * FROM customers WHERE id = %s', id)
        result = cursor.fetchone()
        customer.append({'id': result[3], 'first_name': result[0], 'last_name': result[1], 'email': result[2]})
        return jsonify(customer)
    except Exception as e:
        print (e)
        return "Couldn't find customer", 404

@app.route('/api/customers', methods=['POST'])
def post_customer():
    first_name=request.json['first_name']
    last_name=request.json['last_name']
    email=request.json['email']
   
    sql_str = 'INSERT INTO customers (first_name,last_name,email) VALUES(%s,%s,%s)'
    cursor.execute(sql_str,[first_name, last_name, email])
    conn.commit()
    cursor.execute('SELECT * FROM customers WHERE customers.id = @@IDENTITY')
    result = cursor.fetchone()

    customer = {
        'id':           result[3],
        'first_name':   result[0],
        'last_name':    result[1],
        'email':        result[2]
    }
    return jsonify(customer)


@app.route('/api/customers/update/<int:id>', methods=['POST'])
def update_customer(id):
    # getting update values
    try:
        _json = request.json
        #_id = _json['id']
        _first_name=_json['first_name']
        _last_name=_json['last_name']
        _email=_json['email']

        if id and _first_name and _last_name and _email and request.method == 'POST':
            sql = "UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE id=%s"
            data = (_first_name, _last_name, _email, id,)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            return resp, 200
        else:
            return 'Not found', 404
    except Exception as e:
        print (e)
        return 'An exception occured', 404

@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        sql = "DELETE FROM customers WHERE id = %s"
        data = (id,)
        cursor.execute(sql,data)
        conn.commit()
        resp = jsonify('User deleted successfully')
        return resp, 200
    except Exception as e:
        print (e)
        return 'Delete unsuccessful', 404
'''
@app.route('/api/products', methods=['GET'])
def get_all_products():
    product_list = []
    
    cursor.execute('SELECT products.id, products.name, products.description, products.price AS "price in SEK", categories.name AS category, vendors.name AS vendor FROM products INNER JOIN vendors ON vendors.vendor_id = products.vendor_id INNER JOIN categories ON categories.category_id = products.category_id;')
    products = cursor.fetchall()
    for row in products:
        product_list.append({'id': row[0], 'name': row[1], 'description': row[2], 'price': row[3], 'category': row[4], 'vendor': row[5]})
    return jsonify(product_list)

@app.route('/api/products/<int:id>', methods=['GET'])
def get_one_product(id):
    product = []
    try:
        cursor.execute('SELECT products.id, products.name, products.description, products.price AS "price in SEK", categories.name AS category, vendors.name AS vendor FROM products INNER JOIN vendors ON vendors.vendor_id = products.vendor_id INNER JOIN categories ON categories.category_id = products.category_id WHERE products.id = %s', id)
        result = cursor.fetchone()
        product.append({'id': result[0], 'name': result[1], 'description': result[2], 'price': result[3], 'category': result[4], 'vendor': result[5]})
        return jsonify(product)
    except Exception as e:
        print (e)
        return "Couldn't get product", 404
'''

if __name__ == "__main__":
    app.run(debug=True)