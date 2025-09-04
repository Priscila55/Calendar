# store the standard roots for out website
from flask import Blueprint, render_template 
from flask_login import login_required

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

"""Route for calendar"""
@views.route('/calendar')
@login_required
def calendar():
    return render_template("calendar.html")

"""Route for profile"""
@login_required
@views.route('/profile')
def profile():
    return render_template("profile.html")

# get the data from the calendar 
@views.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    
