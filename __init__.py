from flask import Flask, current_app
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

mysql = MySQL()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = 'auth.login'

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
    def is_authenticated(self): return True
    def is_active(self): return True
    def is_anonymous(self): return False
    def get_id(self): return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1])
    return None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Thisisasecretkey'
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'calendar'

    mysql.init_app(app)
    login_manager.init_app(app)
    app.mysql = mysql
    bcrypt.init_app(app)

    from .views import views
    from .auth import auth
    from .calendar_routes import calendar_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(calendar_bp, url_prefix='/')

    return app
