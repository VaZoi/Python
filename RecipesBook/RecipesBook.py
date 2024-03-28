from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import secrets
import smtplib
from email.mime.text import MIMEText
import hashlib
import base64
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'recipesBook'
app.config['SECRET_KEY'] = secrets.token_hex(16)

mysql = MySQL(app)
app.secret_key = app.config['SECRET_KEY']
bcrypt = Bcrypt(app)

def delete_old_unconfirmed_accounts():
    try:
        connection = mysql.connection
        cursor = connection.cursor()

        cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=4)

        query = "DELETE FROM users WHERE status = 'Unconfirmed' AND confirmation_sent_at < %s"
        cursor.execute(query, (cutoff_date,))

        connection.commit()
        cursor.close()
    except Exception as e:
        print("Error deleting old unconfirmed accounts:", e)

@app.route('/', methods=['GET', 'POST'])
def home():
    delete_old_unconfirmed_accounts()
    print("Home route accessed")
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT status FROM users WHERE username = %s", (session['username'],))
        user_status = cur.fetchone()[0]
        cur.close()

        if user_status == 'Unconfirmed':
            message = "You need to confirm your email. Please check your inbox for the confirmation email."
            return render_template('home.html', username=session['username'], message=message)
        
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
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_username = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_email = cur.fetchone()
        cur.close()

        if existing_username:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        elif existing_email:
            flash('Email already exists. Please use a different one or login.', 'danger')
            return redirect(url_for('register'))
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            token = generate_confirmation_token(email)
            print("Generated token:", token)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password_hash, status, token) VALUES (%s, %s, %s, %s, %s)",
                        (username, email, hashed_password, 'Unconfirmed', token))
            mysql.connection.commit()
            cur.close()

            send_confirmation_email(email, token)

            flash('Registration successful! Please check your email for confirmation.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

def generate_confirmation_token(email):
    secret_key = b'AYg76Axvitr6PuReL_jHv5U0k5MTfhHj9QfzIzWY32E'
    email_bytes = email.encode()

    token = email_bytes + secret_key

    hashed_token = hashlib.sha256(token).digest()

    encoded_token = base64.urlsafe_b64encode(hashed_token).decode()

    return encoded_token

def decode_token(token):
    try:
        decoded_token_bytes = base64.urlsafe_b64decode(token.encode())
        secret_key = b'AYg76Axvitr6PuReL_jHv5U0k5MTfhHj9QfzIzWY32E'
        email_length = len(decoded_token_bytes) - len(secret_key)
        email_bytes = decoded_token_bytes[:email_length]
        return email_bytes.decode('utf-8', errors='replace')
    except Exception as e:
        print("Error decoding token:", e)
        return None


def send_confirmation_email(email, token):
    subject = "Confirmation Email"
    body = """
    Thank you for registering with RecipesBook!

    Please click the following link to confirm your account:
    http://localhost:5000/confirm_email?token={}

    Please note that if your account remains unconfirmed for 4 weeks, it will be automatically deleted from our system for security purposes.
    """.format(token)

    sender = "vazodevelopment@gmail.com"
    password = input("What is your password?\n")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, email, msg.as_string())
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET confirmation_sent_at = %s WHERE email = %s", (datetime.datetime.now(), email))
    mysql.connection.commit()
    cur.close()
    print("Confirmation email sent!")

@app.route('/confirm_email', methods=['GET'])
def confirm_email():
    token = request.args.get('token')

    cur = mysql.connection.cursor()
    cur.execute("SELECT email, token, status FROM users WHERE token = %s", (token,))
    row = cur.fetchone()

    if row:
        email, db_token, status = row
        if db_token == token:
            if status == 'Unconfirmed':
                cur.execute("UPDATE users SET status = 'confirmed' WHERE email = %s", (email,))
                mysql.connection.commit()
                cur.close()
                flash('Email confirmed successfully!', 'success')
            else:
                flash('Email already confirmed!', 'info')
        else:
            flash('Invalid token!', 'danger')
    else:
        flash('No token found!', 'danger')

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
