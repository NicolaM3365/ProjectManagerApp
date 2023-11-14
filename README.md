# Project Manager

This is a simple web application for managing projects and tasks, built using Flask. It allows users to create, view, edit, and delete projects and tasks, and includes user authentication for secure access.

## Features

- **User authentication** Secure login and logout functionality.
- **TODO Gravatar profile picture integration**.
- **Project and task management**:
  - Create new projects.
  - View existing projects and their tasks.
  - Delete projects.
  - Create, view, edit, and delete tasks for projects.
- Search Functionality: Search for projects using specific criteria.
- Live Statistics: View statistical data related to projects.

- Database Integration
This application is integrated with a PostgreSQL database, which stores all user, project, and task data. PostgreSQL provides robust, scalable, and secure data storage and management for the application.

## Live Application

The application is deployed and can be accessed [here](https://projectmanagerapp-hyc4.onrender.com).

## Repository

Source code available on [GitHub](https://github.com/NicolaM3365/ProjectManagerApp)

## Installation and Running

### Requirements
requirements.txt

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NicolaM3365/ProjectManagerApp.git

2. **Navigate to the project directory:**
    cd ProjectManagerApp

3. **Install the necessary packages:**
    pip install -r requirements.txt

4. **Run the application:**
    python app.py

5. **Access the application:**
    Open a web browser and visit http://localhost:5000. n
    
## Usage

- Home Page: The main route '/' directs to the login page or the home page if logged in and displays all projects
- User Authentication: Use '/login' for login and '/logout' for logout.
- Search Projects: Utilize the search functionality via '/search'.
- Task Management: Access project tasks through '/project/<project_id>'.


## Notes

- Before deploying to production, make sure to replace `app.secret_key` with a strong secret key. 

- Example User
- Username: Nicola1
- Password: password1
- Once logged in, navigate to the project by going to http://localhost:5000. Click on "Water Conservation Study" ('/project/4') to manage the project and tasks.

- venv - set up using ANACONDA -   very many requirements / complicated - couldn't pip install  eg psycopg (postgres engine) inside ven - so opted to omit venv.