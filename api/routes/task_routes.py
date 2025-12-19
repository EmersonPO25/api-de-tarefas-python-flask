from flask import Blueprint, request, jsonify
from api.models.task_model import Task
from api.controllers.task_controller import (
    create_task,
    get_all_tasks,
    update_task,
    delete_task
)

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/tasks", methods=["POST"])
def create():
    data = request.get_json()
    task = create_task(data)
    return jsonify(task.to_dict()), 201


@task_bp.route("/tasks", methods=["GET"])
def list_all():
    done_param = request.args.get("done")

    if done_param is not None:
        done_param = done_param.lower() == "true"

    tasks = get_all_tasks(done_param)
    return jsonify([t.to_dict() for t in tasks])


@task_bp.route("/tasks/<int:id>", methods=["PUT"])
def update(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task = update_task(task, data)
    return jsonify(task.to_dict())


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete(id):
    task = Task.query.get_or_404(id)
    delete_task(task)
    return "", 204
