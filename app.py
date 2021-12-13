from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from pymysql import OperationalError
from pymysql.cursors import DictCursor
from pymysql.err import ProgrammingError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mysql = MySQL(app)

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'granja'


def insertIntoDB(sql):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid


try:
    cursor = mysql.connect().cursor(cursor=DictCursor)
except OperationalError as error:
    code, msg = error.args
    print("_" * 100)
    print(msg)
    print("Verificar si la DB está ejecutándose")
    print("_" * 100)


@app.route('/')
def index():
    return '<h2>Esto es una API.</h2> \
            <p><a href="/products">/products</a></p> \
            <p><a href="/orders">/orders</a></p> \
            '


@app.route('/products')
def products():
    sql = 'select * from products where is_deleted = 0;'
    try:
        cursor.execute(sql)
        response = cursor.fetchall()
    except ProgrammingError as error:
        code, msg = error.args
        response = (code, msg)
    return jsonify(response)


@app.route('/products/<string:id>')
def getProductById(id):
    sql = f'select * from products where id = {id} and is_deleted = 0;'
    response = {"error": False, "data": None}
    try:
        cursor.execute(sql)
        response['data'] = cursor.fetchall()
    except:
        response['error'] = True
    return jsonify(response)


@app.route('/orders', methods=['GET', 'POST'])
def getOrders():
    if request.method == 'GET':
        sql = 'select * from orders'
        response = {"error": False, "data": None}
        try:
            cursor.execute(sql)
            response['data'] = cursor.fetchall()
        except:
            response['error'] = True
        return jsonify(response)

    elif request.method == 'POST':
        res = request.json
        try:
            sql = f'insert into orders(total, customer_id) values ({res["total"]}, 1);'
            orderId = insertIntoDB(sql)

            for prod in res["products"]:
                sql = f'insert into order_details(order_id, product_id, quantity) values ({orderId}, {prod["id"]}, {prod["quantity"]});'
                insertIntoDB(sql)
            return {"error": False, "data": res}
        except BaseException as e:
            print(e)
            return {"error": True, "data": None}


@app.route('/orders/<string:id>')
def getOrderById(id):
    sql = f'select * from order_details where order_id = {id}'
    response = {"error": False, "data": None}
    try:
        cursor.execute(sql)
        response['data'] = cursor.fetchall()
        print(response['data'])
    except:
        response['error'] = True
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
