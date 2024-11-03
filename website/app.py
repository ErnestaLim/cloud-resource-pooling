from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Database configuration
db_config = {
    'user': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'host': os.getenv('DB_HOST', '127.0.0.1:3306'),
    'database': os.getenv('DB_NAME', 'cloud')
}

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for Flask-Login


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    @staticmethod
    def get_user_by_email(email):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM User WHERE user_email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()
        if user_data:
            return User(user_data['user_id'], user_data['user_email'], user_data['user_password'])
        return None


@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    if user_data:
        return User(user_data['user_id'], user_data['user_email'], user_data['user_password'])
    return None


# Database connection helper function


def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Route for the index page


@app.route('/')
def index():
    return render_template('index.html')

# Route for the downloads page


@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

# Route for the leaderboard page


@app.route('/leaderboard')
def leaderboard():
    connection = get_db_connection()
    if not connection:
        flash('Unable to connect to the database.', 'danger')
        return redirect(url_for('index'))

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT app_name, app_avg, app_ifeval, app_bbh, app_mathlvl5, app_gpqa, app_musr, app_mmlupro FROM Application"
        )
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f'Database error: {err}', 'danger')
        data = []
    finally:
        cursor.close()
        connection.close()

    return render_template('leaderboard.html', data=data)

# Route for the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_user_by_email(email)

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


# Route for the register page


# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')

        connection = get_db_connection()
        if not connection:
            flash('Unable to connect to the database.', 'danger')
            return redirect(url_for('register'))

        cursor = connection.cursor()
        try:
            # Insert user into the database without the user_name field
            cursor.execute(
                "INSERT INTO User (user_email, user_password) VALUES (%s, %s)",
                (email, hashed_password)
            )
            connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')

# Route for the logout page


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
