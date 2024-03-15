from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import secrets

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'recipesBook'
app.config['SECRET_KEY'] = secrets.token_hex(16)

mysql = MySQL(app)
app.secret_key = app.config['SECRET_KEY']
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Home route accessed")
    if 'username' in session:
        # Fetch recipes from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM recipes")
        columns = [col[0] for col in cur.description]
        recipes = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

        return render_template('home.html', username=session['username'], recipes=recipes)
    else:
        return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    return render_template('recipes.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

