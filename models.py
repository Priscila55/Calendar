from flask import Flask
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'calendar'  
    
    app.config['MYSQL_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
    
    # Initialize MySQL
    mysql = MySQL(app)
    app.mysql = mysql 

    # Register Blueprint
    app.register_blueprint(auth)
    
    mysql.init_app(app)
    
    return app

# get the user by email 
def get_user_by_email(mysql, email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, email, password FROM users where email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user 

def create_user(mysql, username, email, password):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error inserting user: {e}")
    finally:
        cursor.close()

# get goals by user 
def get_goals_by_user(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, goal_name, description, start_date, end_date, status FROM goals WHERE user_id = %s", (user_id))
    goals = cursor.fetchall()
    cursor.close()
    return goals 

# get goals by id
def get_goal_by_id(mysql, goal_id):
   cursor = mysql.connection.cursor()
   cursor.execute("SELECT id, goal_name, description, start_date, end_date, status FROM goals WHERE user_id = %s", (goal_id))
   goal = cursor.fetchall()
   cursor.close()
   return goal 