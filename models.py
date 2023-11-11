

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()



""""each project has a name, description, and manager and several tasks.
Each task has a description and belongs to a project.
The owner of a project is a user."""
"write a class for each of these entities"

# class User:
#     def __init__(self, name, id=None):
#         self.name = name
#         self.id = id



#TO DO check db.Column versus db.mapped_column
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # specify the table name explicitly
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True)
    # SECURITY NOTE: Don't actually store passwords like this in a real system!
    password = db.mapped_column(db.String(80))

    def __str__(self):
        return self.username
    



class Task(db.Model):
        __tablename__ = 'tasks'  # specify the table name explicitly
        task_id = db.mapped_column(db.Integer, primary_key=True)
        name = db.mapped_column(db.String(100), nullable=False)
        description = db.mapped_column(db.String(100), nullable=False)
        status = db.mapped_column(db.String(100), nullable=False)
        # assigned_to = db.mapped_column(db.String(100), nullable=False)
        created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
        project_id = db.mapped_column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)
        project = db.relationship('Project', backref=db.backref('tasks', lazy=True))
        managed_task_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        managed_task = db.relationship('User', backref=db.backref('tasks', lazy=True))
        
        
        
        def __str__(self):
            return self.name
        

class Project(db.Model):
        __tablename__ = 'projects'  # specify the table name explicitly
        project_id = db.mapped_column(db.Integer, primary_key=True, autoincrement=True)
        name = db.mapped_column(db.String(100), nullable=False)
        description = db.mapped_column(db.String(100), nullable=False)
        status = db.mapped_column(db.String(100), nullable=False)
        created_at = db.mapped_column(db.DateTime, default=datetime.utcnow)
        managed_project_id = db.mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        managed_project = db.relationship('User', backref=db.backref('projects', lazy=True))

        def add_task(self, task):
            self.tasks.append(task)

        def total_tasks(self):
            return len(self.tasks)

        def completed_tasks(self):
            return len([task for task in self.tasks if task.status == "Completed"])
        
        @staticmethod
        def get_project_lengths():
            # An example of how to use raw SQL inside a model
            sql = text("SELECT length(name) + length(description) FROM projects")
            return db.session.execute(sql).scalars().all()  # Returns just the integers



        