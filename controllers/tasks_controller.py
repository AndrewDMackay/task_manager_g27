import re
from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import task_repository
from repositories import user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks", __name__)

# Index..
# GET '/tasks/'

@tasks_blueprint.route("/tasks", strict_slashes=False, methods=['GET'])
def tasks():
    tasks = task_repository.select_all()
    return render_template("tasks/index.html", all_tasks = tasks)

# NEW
# GET '/tasks/new'
# Returns an HTML form to the browser..

@tasks_blueprint.route("/tasks/new", strict_slashes=False, methods=['GET'])
def new_task():
    users = user_repository.select_all()
    return render_template("tasks/new.html", all_users = users)

# CREATE
# POST '/tasks/'
# Receives the data from the form to insert into the database..

@tasks_blueprint.route("/tasks", strict_slashes=False, methods=['POST'])
def create_task():
    description = request.form['description']
    user_id = request.form['user_id']
    duration = request.form['duration']
    completed = request.form['completed']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed)
    task_repository.save(task)
    return redirect('/tasks')

# SHOW
# GET '/tasks/<id>'

@tasks_blueprint.route("/tasks/<id>", strict_slashes=False, methods=['GET'])
def show_task(id):
    task = task_repository.select(id)
    return render_template('tasks/show.html', task = task)

# EDIT
# GET '/tasks/<id>/edit'

@tasks_blueprint.route("/tasks/<id>/edit", strict_slashes=False, methods=['GET'])
def edit_task(id):
    task = task_repository.select(id)
    users = user_repository.select_all()
    return render_template('tasks/edit.html', task = task, all_users = users)

# UPDATE
# PUT '/tasks/<id>'
@tasks_blueprint.route("/tasks/<id>", strict_slashes=False, methods=['POST'])
def update_task(id):
    description = request.form['description']
    user_id = request.form['user_id']
    duration = request.form['duration']
    completed = request.form['completed']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed, id)
    task_repository.update(task)
    return redirect('/tasks')

# DELETE
# DELETE '/tasks/<id>'

@tasks_blueprint.route("/tasks/<id>/delete", strict_slashes=False, methods=['POST'])
def delete_task(id):
    task_repository.delete(id)
    return redirect('/tasks')