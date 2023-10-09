# Project Manager with Chat Functionality

This is a simple web application for managing projects and tasks. It also includes a real-time chat feature.

## Features

- **User authentication** (login/logout).
- **Gravatar profile picture integration**.
- **Project and task management**:
  - Create new projects.
  - View existing projects and their tasks.
  - Delete projects.
  - Create, view, edit, and delete tasks for projects.
- **Real-time chat** feature using Flask-SocketIO.

## Live Application

The application is deployed and can be accessed [here](https://projectmanagerapp.onrender.com).

## Repository

Source code available on [GitHub](https://github.com/NicolaM3365/ProjectManager11_09_23).

## Installation and Running

### Requirements

- Python 3.x
- Flask
- Flask-SocketIO

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NicolaM3365/ProjectManager11_09_23.git

2. **Navigate to the root directory:**
    cd ProjectManager11_09_23

3. **Install the necessary packages:**
    cd ProjectManager11_09_23

4. **Run the application:**
    python app.py

5. **Access the application:**
    Open a web browser and visit http://localhost:8080/.

## Usage

- The main route `'/'` will either prompt you for login or show the home page if you're already logged in.
- Use the `/login` route to login. Logging in allows you to view the dashboard and participate in the chat.
- The `/dashboard` route shows the list of all projects including links to project tasks.
- Use the chat functionality by navigating to `/chat_home`.

## Notes

- Before deploying to production, make sure to replace `app.secret_key` with a strong secret key.



