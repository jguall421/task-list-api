from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import create_model, get_models_with_filters, validate_model


bp = Blueprint("goal_bp", __name__, url_prefix= "/goals")
#Create a Goal: Invalid Goal With Missing Title: 400
#Create a Goal: Valid Goal: 201
@bp.post("")
def create_new_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return {
        "details": "Invalid data"
    }, 400

    return create_model(Goal, request_body)
#Get Goals: Getting Saved Goals:200
@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


# #Get Goals: No Saved Goals:  200

# @goal_bp.get("")
# def get_no_saved_goals():
#     goal = validate_task()
#     return goal.to_dict()


#Get One Goal: One Saved Goal: 200
@bp.get("/<goal_id>")
def get_one_saved_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

#Update Goal: 204
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

#Delete Goal: Deleting a Goal: 204
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# #Sending a List of Task IDs to a Goal: 200 OK
# @bp.post("/<goal_id>/tasks")
# def create_tasks_with_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     request_body = request.get_json()
#     request_body["goal_id"] = goal.id
#     return create_model(Task, request_body)
# #Getting Tasks of One Goal: 200 OK
# @bp.get("/<goal_id>/tasks")
# def get_tasks_by_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     response = [task.to_dict() for task in goal.tasks]
#     return response
# #Getting Tasks of One Goal: No Matching Tasks: 200 OK
# @bp.get("/<goal_id>/tasks")
# def get_tasks_for_specific_goal_no_matching_tasks(goal_id):
#     pass

# #Getting Tasks of One Goal: No Matching Goal: 404 Not Found
# @bp.get("/<goal_id>/tasks")
# def get_tasks_for_specific_goal_no_goal():
#     pass

#POST /goals/<goal_id>/tasks
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

# GET /goals/<goal_id>/tasks
# Case 1: Goal exists and has tasks
# @bp.get("/<goal_id>/tasks")
# def get_tasks_by_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     return goal.to_dict(), 200


# # GET /goals/<goal_id>/tasks/no_tasks
# # Case 2: Goal exists but has no tasks
# @bp.get("/<goal_id>/tasks/no_tasks")
# def get_tasks_for_goal_no_tasks(goal_id):
#     goal = validate_model(Goal, goal_id)
#     return goal.to_dict(), 200


# # GET /goals/<goal_id>/tasks/missing_goal
# # Case 3: Goal does not exist
# @bp.get("/<goal_id>/tasks/missing_goal")
# def get_tasks_for_missing_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     response = goal.to_dict()

#     if not goal.tasks:
#         response["tasks"] = []
#     # response = {
#     #     "id": goal.id,
#     #     "title": goal.title,
#     #     "tasks": []
#     # }
#     return response, 200
