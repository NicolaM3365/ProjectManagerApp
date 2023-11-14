from statistics import median, mean

# Your Flask app setup and routes go here

from flask import Flask, jsonify, flash, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)


# from sqlalchemy import func
import sqlalchemy

import hashlib


import pandas as pd
import json
import sqlite3
import os

from models import User, Project, Task, db


# # A secret key is needed to use sessions - it prevents users from modifying the cookie.
# app.secret_key = "Replace me with a real secret key for production use"


app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py


login_manager = LoginManager(app)
login_manager.login_view = "login_page"

with app.app_context():
    db.init_app(app)
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def allow_edit(project):
    return project.managed_project == current_user




# TO DO "" or ''
def gravatar_url(username, size=100, default='identicon', rating='g'):
    url = 'https://secure.gravatar.com/avatar'
    hash = hashlib.md5(username.lower().encode('utf-8')).hexdigest()
    return f'{url}/{hash}?s={size}&d={default}&r={rating}'


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)  # Get the page number from query parameters
    per_page = 8  # Number of projects per page (2 rows of 4 projects)
    projects = Project.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("index.html", projects=projects)


@app.route("/search")
def search():
    search_query = request.args.get('query', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Number of projects per page

    query = Project.query
    if search_query:
        query = query.filter(
            Project.name.ilike(f'%{search_query}%') | 
            Project.description.ilike(f'%{search_query}%') |
            Project.status.ilike(f'%{search_query}%') |
            Project.managed_project.has(User.username.ilike(f'%{search_query}%'))
        )

    paginated_projects = query.paginate(page=page, per_page=per_page, error_out=False)

    projects_data = [{'project_id': project.project_id,
                      'name': project.name,
                      'description': project.description,
                      'status': project.status,
                      'managed_project': project.managed_project.username if project.managed_project else None}
                     for project in paginated_projects.items]

    return jsonify({'projects': projects_data, 'has_next': paginated_projects.has_next})



@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_action():
    username = request.form["username"]
    password = request.form["password"]
    if User.query.filter_by(username=username).first():
        flash(f"The username '{username}' is already taken")
        return redirect(url_for("register_page"))

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash(f"Welcome {username}!")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_action():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f"No such user '{username}'")
        return redirect(url_for("login_page"))
    if password != user.password:
        flash(f"Invalid password for the user '{username}'")
        return redirect(url_for("login_page"))

    login_user(user)
    flash(f"Welcome back, {username}!")
    return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout_page():
    return render_template("logout.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout_action():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("index"))  # TODO: Fix the 'next' functionality





@app.route("/create", methods=["GET"])
@login_required
def create_project_page():
    return render_template("create_project.html")


@app.route("/create", methods=["POST"])
@login_required
def create_project_action():
    project = Project(
        name=request.form["name"],
        description=request.form["description"],
        status=request.form["status"],
        managed_project=current_user,
    )
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("index"))




@app.route("/project/<int:project_id>")
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project.html", project=project, allow_edit=allow_edit(project))


@app.route("/edit/<int:project_id>", methods=["GET"])
@login_required
def edit_page(project_id):
    project = Project.query.get_or_404(project_id)
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to edit it")
        return redirect(url_for("project", project_id=project.project_id))

    return render_template("edit.html", project=project)


@app.route("/edit/<int:project_id>", methods=["POST"])
@login_required
def edit_action(project_id):
    project = Project.query.get_or_404(project_id)
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to edit it")
        return redirect(url_for("project", project_id=project.project_id))

    project.name = request.form["name"]
    project.description = request.form["description"]
    db.session.commit()
    return redirect(url_for("project", project_id=project.project_id))


@app.route("/delete/<int:project_id>", methods=["GET"])
@login_required
def delete_page(project_id):
    project = Project.query.get_or_404(project_id)
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to delete it")
        return redirect(url_for("project", project_id=project.project_id))

    return render_template("delete.html", project=project)


@app.route("/delete/<int:project_id>", methods=["POST"])
@login_required
def delete_action(project_id):
    project = Project.query.get_or_404(project_id)
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to delete it")
        return redirect(url_for("project", project_id=project.project_id))
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("index"))






# Assuming Task model is defined and linked to Project

@app.route("/edit_task/<int:project_id>/<int:task_id>", methods=["GET"])
@login_required
def edit_task_page(project_id, task_id):
    task = Task.query.get_or_404(project_id, task_id)
    project = task.project
    if not allow_edit(project):
        flash(f"Only the project's manager ({project.managed_project}) is allowed to edit its tasks")
        return redirect(url_for("project", project_id=project.project_id))

    return render_template("edit_task.html", task=task)

@app.route("/edit_task/<int:project_id>/<int:task_id>", methods=["POST"])
@login_required
def edit_task_action(project_id, task_id):
    task = Task.query.get_or_404(project_id, task_id)
    project = task.project
    if not allow_edit(project):
        flash(f"Only the project's manager ({project.managed_project}) is allowed to edit its tasks")
        return redirect(url_for("project", project_id=project.project_id))

    task.name = request.form["name"]
    task.description = request.form["description"]
    # Add other task fields as needed
    db.session.commit()
    return redirect(url_for("project", project_id=project.project_id))

# Add similar routes for task deletion if necessary

@app.route("/delete_task/<int:task_id>", methods=["GET"])
@login_required
def delete_task_page(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to delete its tasks")
        return redirect(url_for("project", project_id=project.project_id))

    return render_template("delete_task.html", task=task, project=project)


@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task_action(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    if not allow_edit(project):
        flash(f"Only this project's manager ({project.managed_project}) is allowed to delete its tasks")
        return redirect(url_for("project", project_id=project.project_id))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("project", project_id=project.project_id))












@app.route("/stats")
def stats():
    project_lengths = Project.get_project_lengths()
    projects_per_month = Project.projects_per_month()  
    recent_projects = Project.recent_projects()        

    if project_lengths:
        return render_template(
            "stats.html",
            projects_exist=True,
            average_length=mean(project_lengths),
            median_length=median(project_lengths),
            max_length=max(project_lengths),
            min_length=min(project_lengths),
            total_length=sum(project_lengths),
            projects_per_month=projects_per_month,  # Add this line to pass the data to your template
            recent_projects=recent_projects         # Add this line to pass the data to your template
        )
    else:
        return render_template(
            "stats.html", 
            projects_exist=False,
            projects_per_month=projects_per_month,  # Add this line to pass the data to your template
            recent_projects=recent_projects         # Add this line to pass the data to your template
        )


    

    
def load_data_to_db(json_file_path):
    # Check if the database is already populated
    if Project.query.first():
        print('The database is already populated. Skipping data loading.')
        return

    # Read the JSON file into Python
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    # Create a set of existing user IDs for quick lookup
    existing_user_ids = {user.id for user in User.query.all()}

    # Iterate over projects and tasks, and add them to the database
    for proj in json_data['projects']:
        project = Project(
            project_id=proj['project_id'],
            name=proj['name'],
            description=proj['description'],
            status=proj['status'],
            managed_project_id=proj['managed_project_id']
        )
        db.session.add(project)
        db.session.flush()  # Flush to assign the project_id before adding tasks

        # Load the tasks related to the project
        for task_data in proj['tasks']:
            # Verify the managed_task_id exists
            managed_task_id = task_data.get('managed_task_id')
            if managed_task_id not in existing_user_ids:
                print(f'User ID {managed_task_id} does not exist. Skipping task ID {task_data["task_id"]}.')
                continue

            task = Task(
                task_id=task_data['task_id'],
                name=task_data['name'],
                description=task_data['description'],
                status=task_data['status'],
                project_id=project.project_id,
                managed_task_id=managed_task_id
            )
            db.session.add(task)

    # Commit the session to save the objects to the database
    db.session.commit()
    print('Data from the JSON file has been loaded into the database.')


if __name__ == "__main__":
    with app.app_context():
         # Use forward slashes for the file path, which work on Windows and Unix systems
         json_file_path = 'C:/Users/Nicola.Mitchell/OneDrive - LifeScientific/Desktop/ProjectManagerApp/data/projects.json'
         load_data_to_db(json_file_path)
    app.run(debug=True)