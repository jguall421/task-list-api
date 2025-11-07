from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import create_model, get_models_with_filters, validate_model


bp = Blueprint("goal_bp", __name__, url_prefix= "/goals")

@bp.post("")
def create_new_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return {
        "details": "Invalid data"
    }, 400

    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_saved_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def create_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    for task in goal.tasks:
        task.goal_id = None

    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }
    return response, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_missing_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()

    if not goal.tasks:
        response["tasks"] = []
    return response, 200

