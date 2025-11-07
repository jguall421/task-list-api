from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from datetime import datetime
from app.models.task import Task
import requests
import os
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint("task_bp", __name__, url_prefix= "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

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

@bp.get("/<task_id>")
def get_one_saved_task(task_id):
    task = validate_model(Task,task_id)
    return task.to_dict()
@bp.put("/<task_id>")
def update_a_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task,id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    # response = task.to_dict()

    if task.completed_at is None:
        task.completed_at = datetime.now()

    db.session.commit()
    json_payload = {
                    'channel': 'task-notifications', 
                    'text':f"Someone just completed the task, {task.title}",
                    'Content-Type':'application/json; charset=utf-8'
                    }
    requests.post('https://slack.com/api/chat.postMessage', 
                  json=json_payload,
                  headers={'Authorization': 'Bearer ' + os.environ.get('SLACK_TOKEN')})
    
    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")
