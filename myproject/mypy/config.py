from flask_mysqldb import MySQL
from mypy import app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mypy'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)