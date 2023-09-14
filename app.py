import json
# from flask import Flask, render_template, request, redirect, url_for

import hashlib


from flask import Flask, jsonify, render_template, request, redirect, url_for, session


app = Flask(__name__)


# A secret key is needed to use sessions - it prevents users from modifying the cookie.
app.secret_key = "Replace me with a real secret key for production use"




# with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\data/projects.json", 'r') as f:
#     data = json.load(f)

# with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\data/projects.json", 'w') as f:
#     json.dump(data, f)

   



def gravatar_url(username, size=100, default='identicon', rating='g'):
    url = 'https://secure.gravatar.com/avatar'
    hash = hashlib.md5(username.lower().encode('utf-8')).hexdigest()
    return f'{url}/{hash}?s={size}&d={default}&r={rating}'


@app.route('/')
def index():
    """Home page for the app."""
    if "username" in session:  # Check if user is logged in
        email = session["username"]
        avatar_url = gravatar_url(email)
        return render_template('index.html', avatar_url=avatar_url)
    else:
        return render_template('index.html')



@app.route("/login", methods=["GET"])
def login():
    """Login page for the app.

    If the user is not logged in, display the login form.
    """
    # If the user is already logged in, redirect back to the home page.
    if "username" in session:
        return redirect(url_for("index"))

    # Otherwise, display the login form.
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_action():
    """Login action for the app (same route as the form)."""
    # Get the username from the form field and store it in the session.
    session["username"] = request.form["username"]

    # Redirect to the home page.
    return redirect(url_for("index"))



@app.route("/logout")
def logout():
    """Logout action for the app.

    This removes the user from the session.

    Note that semantically, this should be a POST request,
    but using GET for logging out is simpler and popular.
    """
    # Get and remove the username from the session.
    # Note that the second argument is used to explicitly ignore a missing cookie,
    # rather than raising an exception.
    session.pop("username", None)

    # Redirect to the home page.
    return redirect(url_for("index"))


# @app.route('/dashboard')
# def dashboard():
#     """Dashboard page for the app."""
#     if "username" in session:  # Check if user is logged in
#         email = session["username"]
#         avatar_url = gravatar_url(email)
#         return render_template('dashboard.html', projects=data['projects'], avatar_url=avatar_url)
#     else:
#         return redirect(url_for('login'))
    

# Dashboard
@app.route('/dashboard')
def dashboard():
    try:
        with open("data/projects.json", 'r') as f:
            local_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error loading project data", 500

    if "username" in session:
        email = session["username"]
        avatar_url = gravatar_url(email)
        return render_template('dashboard.html', projects=local_data['projects'], avatar_url=avatar_url)
    else:
        return redirect(url_for('login'))

# Project page
@app.route('/project/<project_id>')
def project_page(project_id):
    try:
        with open("data/projects.json", 'r') as f:
            local_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error loading project data", 500

    project = next((item for item in local_data['projects'] if str(item['project_id']) == str(project_id)), None)

    
    if project is None:
        return redirect(url_for('dashboard'))

    return render_template('project_page.html', project=project)


""" create a new project with its name and description""" 
@app.route('/new_project', methods=['GET', 'POST'])
def new_project():  
    if request.method == 'POST':
        try:
            with open("data/projects.json", 'r') as f:
                local_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Error loading project data", 500

        new_project = {
            "project_id": request.form.get('project_id'),
            "name": request.form.get('name'),
            "description": request.form.get('description'),
            "tasks": []
        }

        local_data['projects'].append(new_project)

        with open("data/projects.json", 'w') as f:
            json.dump(local_data, f)

        return redirect(url_for('dashboard'))
    else:
        return render_template('new_project.html')







@app.route('/new_task/<project_id>', methods=['GET', 'POST'])
def new_task(project_id):
    if request.method == 'POST':
        try:
            with open("data/projects.json", 'r') as f:
                local_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return "Error loading project data", 500
        
        project = next((item for item in local_data['projects'] if str(item['project_id']) == str(project_id)), None)

        if project is None:
            return redirect(url_for('dashboard'))
        
         # Calculate the next task_id
        if project['tasks']:
            next_task_id = max(task['task_id'] for task in project['tasks']) + 1
        else:
            next_task_id = 1  # First task in the project

        new_task = {
            "task_id": next_task_id,
            "name": request.form.get('name'),
            "description": request.form.get('description'),
            "status": request.form.get('status')
        }

        project['tasks'].append(new_task)

        with open("data/projects.json", 'w') as f:
            json.dump(local_data, f)

        return redirect(url_for('project_page', project_id=project_id))
    else:
        return render_template('new_task.html', project_id=project_id)

""" deleteTask() - deletes a task from a project"""
 
@app.route('/api/delete_task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        with open("data/projects.json", 'r') as f:
            local_data = json.load(f)
    
        
        # Assuming each task has a unique id across all projects
        for project in local_data['projects']:
            task_to_remove = next((item for item in project['tasks'] if str(item['task_id']) == str(task_id)), None)


            if task_to_remove:
                project['tasks'].remove(task_to_remove)
                break

        with open("data/projects.json", 'w') as f:
            json.dump(local_data, f)

        return jsonify({'message': 'Task deleted successfully'}), 200

    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'error': 'Failed to delete task'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)
