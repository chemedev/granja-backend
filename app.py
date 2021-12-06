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
