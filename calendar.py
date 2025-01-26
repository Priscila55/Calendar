from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import get_goals_by_user, get_goal_by_id, create_goal, current_app

calendar = Blueprint('calendar', __name__)

@calendar.route('/goals', method=['GET'])
def view_goals():
    if 'user_id' not in session:
        flash("You need to log in first.", category='error')
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    
    calendar = get_goals_by_user(current_app.mysql, user_id)
    