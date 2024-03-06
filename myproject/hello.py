from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mypy'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# Check if user is logged in
def is_logged_in():
    return 'username' in session

# Home page (Login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Use parameterized query to prevent SQL injection
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], entered_password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid login credentials')

    return render_template('login.html', error=None)

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        entered_password = request.form['password']

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(entered_password)

        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            mysql.connection.commit()
            return redirect(url_for('login'))
        except Exception as e:
            error_message = f"Registration failed: {str(e)}"
            return render_template('register.html', error=error_message)

    return render_template('register.html', error=None)

# Home page (after logging in)
@app.route('/home')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))

    return render_template('home.html', username=session['username'])

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
