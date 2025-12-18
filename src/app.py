"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "chess": {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "programming": {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "gym": {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "basketball": {
        "name": "Basketball Team",
        "description": "Compete in basketball games and tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
        },
        "soccer": {
        "name": "Soccer Club",
        "description": "Play and train in soccer matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "art": {
        "name": "Art Studio",
        "description": "Explore painting, drawing, and visual arts",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
        },
        "drama": {
        "name": "Drama Club",
        "description": "Perform in theater productions and improve acting skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["natalie@mergington.edu", "ryan@mergington.edu"]
        },
        "debate": {
        "name": "Debate Team",
        "description": "Develop public speaking and critical thinking skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["sophie@mergington.edu"]
        },
        "science": {
        "name": "Science Club",
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 20,
        "participants": ["thomas@mergington.edu", "anna@mergington.edu"]
        }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return [{"id": k, "name": v["name"], "description": v["description"], "participants": v["participants"]} for k, v in activities.items()]


@app.post("/activities/{activity_id}/signup")
def signup_for_activity(activity_id: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_id]
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity['name']}"}


@app.delete("/activities/{activity_id}/unregister")
def unregister_from_activity(activity_id: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_id not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_id]
    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not signed up for this activity")
    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity['name']}"}
