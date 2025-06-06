from flask import Flask, render_template, redirect, session, request, make_response, jsonify
import smtplib 
import random
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "abc123"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    otp = db.Column(db.Integer, default=None, nullable=True)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    task_details = db.Column(db.String(500), default=None)
    under_list = db.Column(db.String(100), default="primary")

with app.app_context():
    db.create_all()

def send_otp(email, otp):
    sender_email = "sagarnarigara4@gmail.com"
    sender_password = "elwblkudvfhwzcec"
    
    subject = "SGR OTP Code"
    body = f"Your OTP for To Do app by SGR is: {otp}"
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message)

@app.route('/')
def home():
    if request.cookies.get('username'):
        session['email'] = request.cookies.get('username')
        session['varified'] = True
        return redirect('/tasks')
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html', email=session.get('email', ''), otp=session.get('otp', ''))

@app.route('/otp', methods=['POST'])
def otp():
    session['email'] = request.form['email']
    otp = random.randint(10000000, 99999999)
    session['otp'] = otp
    send_otp(session['email'], otp)
    return redirect('/login')

@app.route('/tasks')
def tasks():
    if not session.get('varified'):
        return redirect('/login')
    if request.cookies.get('username'):
        session['email'] = request.cookies.get('username')
    email = session['email']
    tasks = db.session.execute(db.select(Tasks).where(Tasks.user_email == email)).scalars().all()
    tasks_list = list(set(task.under_list for task in tasks))
    return render_template('tasks.html', task=tasks, tasksList=tasks_list)

@app.route('/verify', methods=['POST'])
def verify():
    if request.method == 'POST' and request.form['otp'] == str(session['otp']):
        session['varified'] = True
        if request.form.get('remember') == 'on':
            resp = make_response(redirect('/'))
            resp.set_cookie('username', session['email'], max_age=60*60*24*30)
            return resp
        return redirect('/tasks')
    session['varified'] = False
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        db.session.add(Tasks(
            user_email=session['email'],
            task=request.form['task'],
            task_details=request.form['details'],
            under_list=request.form['category']
        ))
        db.session.commit()
    return redirect('/tasks')

@app.route('/get_tasks/<category>')
def get_tasks(category):
    tasks = Tasks.query.filter_by(under_list=category).all()
    task_list = [{'id': task.id, 'task_name': task.task} for task in tasks]
    return jsonify(task_list)

@app.route('/delete/<int:id>')
def delete(id):
    task = Tasks.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task = Tasks.query.get(id)
    if not task:
        return redirect('/tasks')
    
    task_name = request.form.get('task')
    task_details = request.form.get('details')
    category = request.form.get('category')

    if task_name:
        task.task = task_name
    if task_details:
        task.task_details = task_details
    if category:
        task.under_list = category

    db.session.commit()
    return redirect('/tasks')

@app.route('/search/<query>')
def search(query):
    tasks = Tasks.query.filter(Tasks.task.ilike(f"%{query}%")).all()
    if not tasks:
        return jsonify([])

    task_list = [{
        "id": task.id,
        "task_name": task.task,
        "task_details": task.task_details
    } for task in tasks]
    
    return jsonify(task_list)

if __name__ == '__main__':
    app.run()