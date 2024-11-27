from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Task
from . import db

tasks = Blueprint('tasks', __name__)

@tasks.route('/')
@login_required
def task_list():
    tasks = Task.query.filter_by(owner_id=current_user.id).all()
    return render_template('task_list.html', tasks=tasks)

@tasks.route('/add', methods=['POST'])
@login_required
def add_task():
    description = request.form['description']
    if description:
        task = Task(description=description, owner_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.task_list'))
    flash('Task description cannot be empty.')
    return redirect(url_for('tasks.task_list'))

@tasks.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.owner_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks.task_list'))
