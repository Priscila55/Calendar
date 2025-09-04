from flask import Blueprint, render_template, request, jsonify, flash, session, current_app, redirect, url_for

calendar_bp = Blueprint('calendar', __name__)

def get_cursor():
    return current_app.mysql.connection.cursor()

@calendar_bp.route('/calendar', methods=['GET'])
def calendar():
    if 'user_id' not in session:
        flash("Please log in to access your calendar.", category='error')
        return redirect(url_for('auth.login'))
    return render_template("calendar.html")

@calendar_bp.route('/get-tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id'] 
    cursor = get_cursor()
    try:
        cursor.execute("SELECT date, content FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        tasks_dict = {task[0]: task[1] for task in tasks}
        return jsonify(tasks_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@calendar_bp.route('/add-task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    date = data.get("date")
    content = data.get("content")
    user_id = session['user_id']

    if not date or not content:
        return jsonify({"error": "Invalid data"}), 400

    cursor = get_cursor()
    try:
        cursor.execute("SELECT id FROM tasks WHERE user_id = %s AND date = %s", (user_id, date))
        existing_task = cursor.fetchone()

        if existing_task:
            cursor.execute(
                "UPDATE tasks SET content = %s WHERE user_id = %s AND date = %s",
                (content, user_id, date)
            )
        else:
            cursor.execute(
                "INSERT INTO tasks (user_id, date, content) VALUES (%s, %s, %s)",
                (user_id, date, content)
            )

        current_app.mysql.connection.commit()
        return jsonify({"message": "Task saved successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
