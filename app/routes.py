from urllib.parse import urlsplit

from flask import render_template, abort, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User

todos = [
    {"id": 1, "title": "Todo1"},
    {"id": 2, "title": "Todo2"},
]


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/tasks")
def all_tasks():
    # later you might want: return render_template("tasks.html", todos=todos)
    return "<h1>List of all tasks</h1>"


# note the <int:task_id> converter here
@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    # find the todo with matching id
    task = next((t for t in todos if t["id"] == task_id), None)
    if task is None:
        abort(404)

    return render_template("task.html", task=task)


@app.route("/new-task")
def new_task():
    return "<h1>New Task</h1>"
