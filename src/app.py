"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from sqlalchemy.orm import Session
from models import get_db, Base, engine
from models.activity import Activity

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Initial activities data - will be used to populate the database
initial_activities = [
    {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "time": "Fridays, 3:30 PM - 5:00 PM",
        "category": "Academic"
    },
    {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "time": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "category": "Academic"
    },
    {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "time": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "category": "Sports"
    },
    {
        "name": "Soccer Team",
        "description": "Join the school soccer team and compete in matches",
        "time": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "category": "Sports"
    },
    {
        "name": "Basketball Team",
        "description": "Practice and play basketball with the school team",
        "time": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "category": "Sports"
    },
    {
        "name": "Art Club",
        "description": "Explore your creativity through painting and drawing",
        "time": "Thursdays, 3:30 PM - 5:00 PM",
        "category": "Arts"
    },
    {
        "name": "Drama Club",
        "description": "Act, direct, and produce plays and performances",
        "time": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "category": "Arts"
    },
    {
        "name": "Math Club",
        "description": "Solve challenging problems and participate in math competitions",
        "time": "Tuesdays, 3:30 PM - 4:30 PM",
        "category": "Academic"
    },
    {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "time": "Fridays, 4:00 PM - 5:30 PM",
        "category": "Academic"
    }
]

def init_db(db: Session = Depends(get_db)):
    """Initialize the database with sample activities if empty"""
    if db.query(Activity).count() == 0:
        for activity_data in initial_activities:
            activity = Activity(**activity_data)
            db.add(activity)
        db.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    db = next(get_db())
    init_db(db)


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities"""
    activities = db.query(Activity).all()
    return [activity.to_dict() for activity in activities]


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Get the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
