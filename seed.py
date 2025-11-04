
from app import create_app, db
from app.models.task import Task
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Plan weekly goals", description="Write down top 3 priorities for the week to stay focused.", completed_at=None)),
    db.session.add(Task(title="Go for a morning walk", description="Get some fresh air and move for at least 20 minutes.", completed_at=datetime(2025, 10, 30))),
    db.session.add(Task(title="Organize workspace", description="Clean desk and remove distractions to improve productivity.", completed_at=None)),
    db.session.add(Task(title="Read a new article about APIs", description="Find one article that explains REST API design best practices.", completed_at=datetime(2025, 10, 28))),
    db.session.add(Task(title="Build Task List API", description="Create endpoints for adding, reading, updating, and deleting tasks.", completed_at=None)),
    db.session.add(Task(title="Test API with Postman", description="Send requests to verify all CRUD routes are working as expected.", completed_at=None)),
    db.session.add(Task(title="Reflect on progress", description="Take 10 minutes to write what went well this week and what can improve.", completed_at=None)),
    db.session.add(Task(title="Share project with a friend", description="Ask for feedback on your Task List API and explain how it works.", completed_at=datetime(2025, 10, 31))),
    db.session.add(Task(title="Backup project files", description="Save project to GitHub and verify all files are pushed correctly.", completed_at=None)),
    db.session.add(Task(title="Celebrate small wins", description="Take a break, enjoy a treat, and recognize your hard work.", completed_at=None)),
    db.session.commit()