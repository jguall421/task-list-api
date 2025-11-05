from flask import Blueprint, abort, make_response, Response, request
from app.db import db
from datetime import datetime
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix= "/tasks")

#Create a Task: Valid Task With null completed_at
#Create a Task: Invalid Task With Missing Data 400
@task_bp.post("")
def create_task():
    
    request_body = request.get_json()
    if not "title" in request_body:
        return {
        "details": "Invalid data"
    }, 400

    if not "description" in request_body:
        return {
        "details": "Invalid data"
    }, 400

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    if new_task.completed_at is None:
        return new_task.to_dict(), 201


#Get Tasks: Getting Saved Tasks 200
@task_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title == title_param)
        
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description == description_param)


    tasks = db.session.scalars(query)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response


#Get One Task: One Saved Task 200
@task_bp.get("/<task_id>")
def get_one_saved_task(task_id):
    task = validate_task(task_id)
    return task.to_dict()

#Update Task 204 
@task_bp.put("/<task_id>")
def update_a_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#Delete Task: Deleting a Task 204
@task_bp.delete("/<id>")
def delete_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


#No Matching Task: Get, Update, and Delete 404
#Get Tasks: No Saved Tasks 200
def validate_task(id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f"Task id({id}) is invalid."}

        abort(make_response(invalid, 400))

    query = db.select(Task).where(Task.id == id)
    task = db.session.scalar(query)

    if not task:
        not_found = {"message": f"Task with id({id}) not found."}
        abort(make_response(not_found, 404))
    
    return task

#Mark Complete on an Incomplete Task
#PATCH request to /tasks/1/mark_complete: 204 No Content
@task_bp.patch("/<task_id>/mark_complete")
def mark_complete_on_incomplete_task(task_id):
    task = validate_task(task_id)
    task.completed_at =  datetime.now()
    db.session.commit()
    return Response(status=204, mimetype="application/json")

# #Mark Incomplete on a Completed Task
# #PATCH request to /tasks/1/mark_incomplete
@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_on_complete_task(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# #Mark Complete on a Completed Task
# #PATCH request to /tasks/1/mark_complete: 204 OK
@task_bp.patch("/<task_id>/mark_complete")
def mark_complete_on_completed_task(task_id):
    task = validate_task(task_id)
    if task.completed_at is None:
        task.completed_at = datetime.now()
    db.session.commit()
    return Response(status=204, mimetype="application/json")

# #Mark Incomplete on an Incomplete Task
# #PATCH request to /tasks/1/mark_incomplete
@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_on_incomplete_task(task_id):
    task = validate_task(task_id)
    if task.completed_at is not None:
        task.completed_at = None 
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# #Mark Complete and Mark Incomplete for Missing Tasks
# #PATCH request to /tasks/1/mark_complete or a PATCH request to /tasks/1/mark_incomplete: 404 Not Found
@task_bp.patch("/tasks/<task_id>/mark_complete")
def test_mark_complete_missing_task(task_id):
    task = validate_task(task_id)
    if task.completed_at is None:
        task.completed_at = datetime.now()
        db.session.commit()
    return Response(status=204, mimetype="application/json")
    
@task_bp.patch("/tasks/<task_id>/mark_incomplete")
def mark_incomplete_missing_task(task_id):
    task = validate_task(task_id)
    if task.completed_at is not None:
        task.completed_at = None
        db.session.commit()
    return Response(status=204, mimetype="application/json")