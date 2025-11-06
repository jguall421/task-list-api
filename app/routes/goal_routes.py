from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from app.models.goal import Goal

goal_bp = Blueprint("goal_bp", __name__, url_prefix= "/goals")
#Create a Goal: Invalid Goal With Missing Title: 400
#Create a Goal: Valid Goal: 201
@goal_bp.post("")
def create_new_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return {
        "details": "Invalid data"
    }, 400

    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()
    return new_goal.to_dict(), 201

#Get Goals: Getting Saved Goals:200
@goal_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title == title_param)
    goals = db.session.scalars(query)
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response

# #Get Goals: No Saved Goals:  200

# @goal_bp.get("")
# def get_no_saved_goals():
#     goal = validate_task()
#     return goal.to_dict()


#Get One Goal: One Saved Goal: 200
@goal_bp.get("/<goal_id>")
def get_one_saved_goal(goal_id):
    goal = validate_task(goal_id)
    return goal.to_dict()

#Update Goal: 204
@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_task(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

#Delete Goal: Deleting a Goal: 204
@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_task(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


#No matching Goal: Get, Update, and Delete:404
def validate_task(id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f"Goal id({id}) is invalid."}

        abort(make_response(invalid, 400))

    query = db.select(Goal).where(Goal.id == id)
    goal = db.session.scalar(query)

    if not goal:
        not_found = {"message": f"Goal with id({id}) not found."}
        abort(make_response(not_found, 404))
    
    return goal