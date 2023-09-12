import json
# from flask import Flask, render_template, request, redirect, url_for

import hashlib


from flask import Flask, jsonify, render_template, request, redirect, url_for, session


app = Flask(__name__)


# A secret key is needed to use sessions - it prevents users from modifying the cookie.
app.secret_key = "Replace me with a real secret key for production use"




# with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\projects.json", 'r') as f:
#     data = json.load(f)

# with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\projects.json", 'w') as f:
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
        with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\projects.json", 'r') as f:
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
        with open("C:\\Users\\Nicola.Mitchell\\OneDrive - LifeScientific\\Desktop\\UCD\\3-Python\\Unit12\\ProjectManager\\data\\projects.json", 'r') as f:
            local_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error loading project data", 500

    project = next((item for item in local_data['projects'] if item['id'] == project_id), None)
    
    if project is None:
        return redirect(url_for('dashboard'))

    return render_template('project.html', project=project)




if __name__ == '__main__':
    app.run(debug=True, port=8080)
