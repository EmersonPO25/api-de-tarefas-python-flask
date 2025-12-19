from api.models.task_model import Task
from api.extensions import db


def create_task(data):
    task = Task(
        title=data["title"],
        description=data.get("description")
    )
    db.session.add(task)
    db.session.commit()
    return task


def get_all_tasks(done=None):
    if done is None:
        return Task.query.all()

    return Task.query.filter_by(done=done).all()


def update_task(task, data):
    if "title" in data:
        task.title = data["title"]

    if "description" in data:
        task.description = data["description"]

    if "done" in data:
        task.done = bool(data["done"])

    db.session.commit()
    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()
