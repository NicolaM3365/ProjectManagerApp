

""""each project has a name, description, and owner and several tasks.
Each task has a description and belongs to a project.
The owner of a project is a user."""
"wrte a class for each of these entities"

class User:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id



class Task:
    def __init__(self, task_id, name, description, status, assigned_to=None):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.assigned_to = assigned_to

class Project:
    def __init__(self, project_id, name, description, tasks=None):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task):
        self.tasks.append(task)

    def total_tasks(self):
        return len(self.tasks)

    def completed_tasks(self):
        return len([task for task in self.tasks if task.status == "Completed"])


        