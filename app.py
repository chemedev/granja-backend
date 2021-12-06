from flask import Flask, jsonify
from flaskext.mysql import MySQL
from pymysql import OperationalError
from pymysql.cursors import DictCursor
from pymysql.err import ProgrammingError

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'granja'

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


if __name__ == '__main__':
    app.run(debug=True)
