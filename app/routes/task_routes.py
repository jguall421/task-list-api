from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from datetime import datetime
from app.models.task import Task
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint("task_bp", __name__, url_prefix= "/tasks")

#Create a Task: Valid Task With null completed_at
#Create a Task: Invalid Task With Missing Data 400
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

#Get Tasks: Getting Saved Tasks 200
@bp.get("")
def get_all_tasks():
    filters = {}
    title = request.args.get("title")
    description = request.args.get("description")
    sort = request.args.get("sort", "asc")

    if title:
        filters["title"] = title
    if description:
        filters["description"] = description

    return get_models_with_filters(Task, filters, sort)

#Get One Task: One Saved Task 200
@bp.get("/<task_id>")
def get_one_saved_task(task_id):
    task = validate_model(Task,task_id)
    return task.to_dict()

#Update Task 204 
@bp.put("/<task_id>")
def update_a_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#Delete Task: Deleting a Task 204
@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task,id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# PATCH /tasks/<task_id>/mark_complete
@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    """Marks a task as complete, regardless of its current state."""
    task = validate_model(Task, task_id)

    if task.completed_at is None:
        task.completed_at = datetime.now()

    db.session.commit()
    return Response(status=204, mimetype="application/json")


# PATCH /tasks/<task_id>/mark_incomplete
@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# #Mark Complete on an Incomplete Task
# #PATCH request to /tasks/1/mark_complete: 204 No Content
# @task_bp.patch("/<task_id>/mark_complete")
# def mark_complete_on_incomplete_task(task_id):
#     task = validate_model(Task,task_id)
#     task.completed_at =  datetime.now()
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")

# # #Mark Incomplete on a Completed Task
# # #PATCH request to /tasks/1/mark_incomplete
# @task_bp.patch("/<task_id>/mark_incomplete")
# def mark_incomplete_on_complete_task(task_id):
#     task = validate_model(Task,task_id)
#     task.completed_at = None
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")


# # #Mark Complete on a Completed Task
# # #PATCH request to /tasks/1/mark_complete: 204 OK
# @task_bp.patch("/<task_id>/mark_complete")
# def mark_complete_on_completed_task(task_id):
#     task = validate_model(Task,task_id)
#     if task.completed_at is None:
#         task.completed_at = datetime.now()
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")

# # #Mark Incomplete on an Incomplete Task
# # #PATCH request to /tasks/1/mark_incomplete
# @task_bp.patch("/<task_id>/mark_incomplete")
# def mark_incomplete_on_incomplete_task(task_id):
#     task = validate_model(Task,task_id)
#     if task.completed_at is not None:
#         task.completed_at = None 
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")


# # #Mark Complete and Mark Incomplete for Missing Tasks
# # #PATCH request to /tasks/1/mark_complete or a PATCH request to /tasks/1/mark_incomplete: 404 Not Found
# @task_bp.patch("/tasks/<task_id>/mark_complete")
# def test_mark_complete_missing_task(task_id):
#     task = validate_model(Task,task_id)
#     if task.completed_at is None:
#         task.completed_at = datetime.now()
#         db.session.commit()
#     return Response(status=204, mimetype="application/json")
    
# @task_bp.patch("/tasks/<task_id>/mark_incomplete")
# def mark_incomplete_missing_task(task_id):
#     task = validate_model(Task, task_id)
#     if task.completed_at is not None:
#         task.completed_at = None
#         db.session.commit()
#     return Response(status=204, mimetype="application/json")