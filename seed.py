
from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

goals = [
    {
        "title": "Health and Wellness",
        "tasks": [
            {
                "title": "Go for a morning walk",
                "description": "Get some fresh air and move for at least 20 minutes.",
                "completed_at": datetime(2025, 10, 30)
            },
            {
                "title": "Drink more water",
                "description": "Aim for 8 glasses of water throughout the day.",
                "completed_at": None
            },
            {
                "title": "Stretch before bed",
                "description": "Spend 10 minutes doing light stretches to improve sleep.",
                "completed_at": None
            }
        ]
    },
    {
        "title": "Professional Growth",
        "tasks": [
            {
                "title": "Read a new article about APIs",
                "description": "Find one article that explains REST API design best practices.",
                "completed_at": datetime(2025, 10, 28)
            },
            {
                "title": "Build Task List API",
                "description": "Create endpoints for adding, reading, updating, and deleting tasks.",
                "completed_at": None
            },
            {
                "title": "Test API with Postman",
                "description": "Send requests to verify all CRUD routes are working as expected.",
                "completed_at": None
            }
        ]
    },
    {
        "title": "Personal Development",
        "tasks": [
            {
                "title": "Plan weekly goals",
                "description": "Write down top 3 priorities for the week to stay focused.",
                "completed_at": None
            },
            {
                "title": "Reflect on progress",
                "description": "Take 10 minutes to write what went well this week and what can improve.",
                "completed_at": None
            },
            {
                "title": "Celebrate small wins",
                "description": "Take a break, enjoy a treat, and recognize your hard work.",
                "completed_at": None
            }
        ]
    }
]

# Tasks not tied to a goal
independent_tasks = [
    {
        "title": "Share project with a friend",
        "description": "Ask for feedback on your Task List API and explain how it works.",
        "completed_at": datetime(2025, 10, 31)
    },
    {
        "title": "Backup project files",
        "description": "Save project to GitHub and verify all files are pushed correctly.",
        "completed_at": None
    }
]


# --- HELPER FUNCTION ---

def get_model_by_field(cls, data_dict, key_name):
    """Prevent duplicate entries by checking if a record already exists by a unique field."""
    value = data_dict[key_name]
    stmt = db.select(cls).where(getattr(cls, key_name) == value)
    return db.session.scalar(stmt)


# --- SEED LOGIC ---

load_dotenv()
my_app = create_app()

with my_app.app_context():

    # Create Goals and their Tasks
    for goal_data in goals:
        goal = get_model_by_field(Goal, goal_data, "title")
        if not goal:
            goal = Goal(title=goal_data["title"])
            db.session.add(goal)
            db.session.flush()  # get goal.id before creating tasks

        for task_data in goal_data["tasks"]:
            task = get_model_by_field(Task, task_data, "title")
            if not task:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    completed_at=task_data["completed_at"],
                    goal_id=goal.id
                )
                db.session.add(task)

    # Add independent (no goal) tasks
    for task_data in independent_tasks:
        task = get_model_by_field(Task, task_data, "title")
        if not task:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                completed_at=task_data["completed_at"],
                goal_id=None
            )
            db.session.add(task)

    db.session.commit()
    print("✅ Database successfully seeded with goals and tasks!")
