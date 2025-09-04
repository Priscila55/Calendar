
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_mysqldb import MySQL
from website.models import get_user_by_email
from website import User, bcrypt
from flask_login import login_user, logout_user


auth = Blueprint('auth', __name__)

def cursor():
    current_app.cursor = current_app.mysql.connection.commit()

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    
        try:
            user = get_user_by_email(current_app.mysql, email)
        
            if not user:
                    flash('Email does not exist.', category='error')
            elif not bcrypt.check_password_hash(user[3], password):
                    flash('Incorrect password.', category='error')
            else:
                    user = User(id =user[0], username=user[1])
                    login_user(user)
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('calendar.calendar'))
        except Exception as e:
            flash(f"An error occurred: {e}", category='error')                
        
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username") 
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        cursor = current_app.mysql.connection.cursor()
        try:
            user = get_user_by_email(current_app.mysql, email)
            if user:
                flash('Email already exists', category='error')
            elif not username or len(username) < 5:
                flash('Username should be greater than 4 characters', category='error') 
            elif not email or len(email) < 3: 
                flash('Email should be greater than 2 characters', category='error') 
            elif password1 != password2:
                flash('Passwords do not match', category='error')
            elif not password1 or len(password1) < 8: 
                flash('Password must be at least 7 characters', category='error') 
            else: 
                    # hash password 
                    hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
                    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)" 
                    cursor.execute(query, (username, email, hashed_password))
                    current_app.mysql.connection.commit()
                    flash('Account created successfully!', category='success')
                    return redirect(url_for('auth.login'))
        except Exception as e:
                    flash(f"Error: {e}", category= 'error')
        finally:
                    cursor.close()
        
    return render_template("signup.html")
                 
@auth.route('/home', methods=['GET'])
def home():
    return render_template("home.html")
