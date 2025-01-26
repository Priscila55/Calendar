from flask import Flask 
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)
    # encrypt or secure cookies and session data in website
    app.config['SECRET_KEY'] = 'Thisisasecretkey'
    
    # MySQL configuration
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'root'  
    app.config['MYSQL_PASSWORD'] = ''  
    app.config['MYSQL_DB'] = 'calendar'
    
    mysql = MySQL(app)
    
    from .views import views
    from .auth import auth 
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    app.mysql = mysql
    
    return app 
