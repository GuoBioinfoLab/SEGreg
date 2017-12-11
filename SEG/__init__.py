from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

print(app.config['MYSQL_HOST'])

app.config.from_object('SEG.settings')

print(app.config['MYSQL_HOST'])

app.url_map.strict_slashes = False


# import SEG.connect
import SEG.controllers
import SEG.models
