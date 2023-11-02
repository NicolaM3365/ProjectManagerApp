from statistics import median, mean


from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

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



# @app.route("/")
# def index():
#     """Home page for the app."""
#     if "username" in session:  # Check if user is logged in
#         email = session["username"]
#         avatar_url = gravatar_url(email)
#         return render_template("index.html", avatar_url=avatar_url, projects=Project.query.all())
#     else:
#         return render_template("index.html")




@app.route("/")
def index():
    return render_template("index.html", projects=Project.query.all())


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














# @app.route("/login", methods=["GET"])
# def login():
#     """Login page for the app.

#     If the user is not logged in, display the login form.
#     """
#     # If the user is already logged in, redirect back to the home page.
#     if "username" in session:
#         return redirect(url_for("index"))

#     # Otherwise, display the login form.
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def login_action():
#     """Login action for the app (same route as the form)."""
#     # Get the username from the form field and store it in the session.
#     session["username"] = request.form["username"]

#     # Redirect to the home page.
#     return redirect(url_for("index"))



# @app.route("/logout")
# def logout():
#     """Logout action for the app.

#     This removes the user from the session.

#     Note that semantically, this should be a POST request,
#     but using GET for logging out is simpler and popular.
#     """
#     # Get and remove the username from the session.
#     # Note that the second argument is used to explicitly ignore a missing cookie,
#     # rather than raising an exception.
#     session.pop("username", None)

#     # Redirect to the home page.
#     return redirect(url_for("index"))


# @app.route('/dashboard')
# def dashboard():
#     """Dashboard page for the app."""
#     if "username" in session:  # Check if user is logged in
#         email = session["username"]
#         avatar_url = gravatar_url(email)
#         return render_template('dashboard.html', projects=data['projects'], avatar_url=avatar_url)
#     else:
#         return redirect(url_for('login'))
    




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


@app.route("/stats")
def stats():
    project_lengths = Project.get_project_lengths()

    if project_lengths:
        return render_template(
            "stats.html",
            projects_exist=True,
            average_length=mean(project_lengths),
            median_length=median(project_lengths),
            max_length=max(project_lengths),
            min_length=min(project_lengths),
            total_length=sum(project_lengths),
        )
    else:
        return render_template("stats.html", projects_exist=False)
    
    
    

    
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
    # with app.app_context():
    #     # Use forward slashes for the file path, which work on Windows and Unix systems
    #     json_file_path = 'C:/Users/Nicola.Mitchell/OneDrive - LifeScientific/Desktop/UCD/project_manager_app/ProjectManager11_09_23/data/projects.json'
    #     load_data_to_db(json_file_path)
    app.run(debug=True)






















































# # Dashboard
# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     try:
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return "Error loading project data", 500

#     # Convert the loaded JSON projects data into Project objects
#     project_objects = []
#     for project_dict in local_data['projects']:
#         tasks = project_dict.get('tasks', [])

#         # Convert tasks into Task objects
#         task_objects = []
#         for task_dict in tasks:
#             task = Task(
#                 task_dict['task_id'],
#                 task_dict['name'],
#                 task_dict['description'],
#                 task_dict['status'],
#                 task_dict.get('assigned_to', None)  # This accounts for if 'assigned_to' is not present
#             )
#             task_objects.append(task)

#         # Now create the Project object
#         project = Project(
#             project_dict['project_id'], 
#             project_dict['name'], 
#             project_dict['description'], 
#             task_objects
#         )
#         project_objects.append(project)
        
#     if "username" in session:
#         email = session["username"]
#         avatar_url = gravatar_url(email)
#         return render_template('dashboard.html', projects=project_objects, avatar_url=avatar_url)
#     else:
#         return redirect(url_for('login'))

# # Project page
# @app.route('/project/<int:project_id>', methods=['GET'])
# def project_page(project_id):
#     try:
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return "Error loading project data", 500

#     project = next((item for item in local_data['projects'] if (item['project_id']) == (project_id)), None)

    
#     if project is None:
#         return redirect(url_for('dashboard'))

#     return render_template('project_page.html', project=project)


# """ create a new project with its name and description""" 
# @app.route('/new_project', methods=['GET', 'POST'])
# def new_project():  
#     if request.method == 'POST':
#         try:
#             with open("data/projects.json", 'r') as f:
#                 local_data = json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError):
#             return "Error loading project data", 500
        
        
#         # Find the largest existing project ID
#         max_id = 0
#         for project in local_data['projects']:
#             if 'project_id' in project and project['project_id'] > max_id:
#                 max_id = project['project_id']

#         # Generate a new unique ID
#         new_project_id = max_id + 1


#         new_project = {
#             "project_id": new_project_id,
#             "name": request.form.get('name'),
#             "description": request.form.get('description')
            
#         }

#         local_data['projects'].append(new_project)

#         with open("data/projects.json", 'w') as f:
#             json.dump(local_data, f)

#         return redirect(url_for('dashboard'))
#     else:
#         return render_template('new_project.html')




# @app.route('/delete_project/<int:project_id>', methods=['POST'])
# def delete_project_route(project_id):
#     try:
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)

#         project_to_remove = next((project for project in local_data['projects'] if project['project_id'] == project_id), None)
        
#         if project_to_remove:
#             local_data['projects'].remove(project_to_remove)

#         with open("data/projects.json", 'w') as f:
#             json.dump(local_data, f)

#         return redirect(url_for('dashboard'))  # Assuming 'index' is your main page's route function

#     except (FileNotFoundError, json.JSONDecodeError):
#         return redirect(url_for('error_route'))  # Assuming 'error_route' is the function name for the error page








# @app.route('/new_task/<int:project_id>', methods=['GET', 'POST'])
# def new_task(project_id):
#     if request.method == 'POST':
#         try:
#             with open("data/projects.json", 'r') as f:
#                 local_data = json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError):
#             return "Error loading project data", 500
        
#         project = next((item for item in local_data['projects'] if (item['project_id']) == (project_id)), None)

#         if project is None:
#             return redirect(url_for('dashboard'))
        
#          # Calculate the next task_id
#         if project['tasks']:
#             next_task_id = max(int(task['task_id']) for task in project['tasks']) + 1
#         else:
#             next_task_id = 1  # First task in the project

#         new_task = {
#             "task_id": next_task_id,
#             "name": request.form.get('name'),
#             "description": request.form.get('description'),
#             "status": request.form.get('status')
#         }

#         project['tasks'].append(new_task)

#         with open("data/projects.json", 'w') as f:
#             json.dump(local_data, f)

#         return redirect(url_for('project_page', project_id=project_id))
#     else:
#         return render_template('new_task.html', project_id=project_id)
        
# """ deleteTask() - deletes a task from a project"""

# @app.route('/delete_task/<int:project_id>/<int:task_id>', methods=['POST'])
# def delete_task(project_id, task_id):
#     try:
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)
    
#         for project in local_data['projects']:
#             if project['project_id'] == project_id:
#                 task_to_remove = next((item for item in project['tasks'] if item['task_id'] == task_id), None)
#                 if task_to_remove:
#                     project['tasks'].remove(task_to_remove)
#                     break

#         with open("data/projects.json", 'w') as f:
#             json.dump(local_data, f)

#         return redirect(url_for('project_page', project_id=project_id))

#     except (FileNotFoundError, json.JSONDecodeError):
#         return redirect(url_for('error_route'))  # Assuming 'error_route' is the function name for the error page


# @app.route('/edit_task_page/<int:project_id>/<int:task_id>', methods=['GET'])
# def edit_task_page(project_id, task_id):
#     try:
#         # Load the existing projects and tasks from the JSON file
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)

#         project_to_edit = next((project for project in local_data['projects'] if project['project_id'] == project_id), None)
#         if not project_to_edit:
#             return redirect(url_for('error_route'))  # Project not found

#         task_to_edit = next((task for task in project_to_edit['tasks'] if task['task_id'] == task_id), None)
#         if not task_to_edit:
#             return redirect(url_for('error_route'))  # Task not found within the specified project

#         return render_template('edit_task.html', project=project_to_edit, task=task_to_edit)

#     except (FileNotFoundError, json.JSONDecodeError):
#         return redirect(url_for('error_route'))  # Redirect to error page if something goes wrong




# @app.route('/find_and_edit_task/<int:project_id>/<int:task_id>', methods=['POST'])
# def find_and_edit_task(project_id, task_id):
#     try:
#         # Load the existing projects and tasks from the JSON file
#         with open("data/projects.json", 'r') as f:
#             local_data = json.load(f)

#         # Variables to keep track of the project and task to edit
#         project_to_edit = None
#         task_to_edit = None

#         # Locate the project using project_id
#         for project in local_data['projects']:
#             if project['project_id'] == project_id:
#                 project_to_edit = project
#                 break

#         if not project_to_edit:
#             return redirect(url_for('error_route'))  # Project not found

#         # Locate the task within that project using task_id
#         task_to_edit = next((task for task in project_to_edit['tasks'] if task['task_id'] == task_id), None)

#         if not task_to_edit:
#             return redirect(url_for('error_route'))  # Task not found within the specified project


#         # Update the task data from form
#         task_to_edit['name'] = request.form['name']
#         task_to_edit['description'] = request.form['description']
#         task_to_edit['status'] = request.form['status']
#         task_to_edit['assigned_to'] = request.form['assigned_to']

#         # Save updated project and tasks data back to the JSON file
#         with open("data/projects.json", 'w') as f:
#             json.dump(local_data, f)

#         return redirect(url_for('project_page', project_id=project_id))
    

#     except (FileNotFoundError, json.JSONDecodeError):
#         return redirect(url_for('error_route'))  # Redirect to error page if something goes wrong

