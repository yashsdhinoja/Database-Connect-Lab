from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

from database.supabase_client import supabase
from database.mongo_client import activity_collection, screen_time_collection, mood_history_collection

app = FastAPI(title="Hybrid Supabase + MongoDB Engine")

# --- Models ---
class UserProfile(BaseModel):
    user_id: str  # UUID string shared across databases
    first_name: str
    last_name: str
    email: str
    age: int

class ActivityLog(BaseModel):
    user_id: str  # Linked UUID
    video_id: str
    video_category: str
    watch_time_seconds: int
    interaction: str  # e.g., "like", "skip", "comment"
    screen_time_session: int  # in minutes

# --- API Endpoints ---

@app.post("/create-user")
def create_user(profile: UserProfile):
    """Stores structured profile data in Supabase."""
    try:
        response = supabase.table("profiles").insert({
            "user_id": profile.user_id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email": profile.email,
            "age": profile.age
        }).execute()
        return {"status": "User created in Supabase", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/log-activity")
def log_activity(activity: ActivityLog):
    """Stores high-frequency activity & screen time logs in MongoDB using the same user_id."""
    
    # 1. Base Document
    activity_doc = activity.dict()
    activity_doc["timestamp"] = datetime.utcnow()

    # 2. Derive mood state based on activity
    detected_mood = "neutral"
    if activity.video_category == "sad" and activity.watch_time_seconds > 12:
        detected_mood = "sad"
    elif activity.video_category == "comedy" and activity.watch_time_seconds > 10:
        detected_mood = "happy"

    activity_doc["detected_mood"] = detected_mood

    # 3. Store in MongoDB
    activity_collection.insert_one(activity_doc)

    # 4. Upsert screen time summary in MongoDB
    screen_time_collection.update_one(
        {"user_id": activity.user_id},
        {
            "$inc": {"total_screen_time_seconds": activity.watch_time_seconds},
            "$set": {"last_active": datetime.utcnow()}
        },
        upsert=True
    )

    return {"status": "Activity logged in MongoDB", "detected_mood": detected_mood}

@app.get("/user-dashboard/{user_id}")
def get_user_dashboard(user_id: str):
    """Fetches combined profile data from Supabase and behavioral logs from MongoDB."""
    
    # Fetch profile from Supabase
    supabase_res = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    if not supabase_res.data:
        raise HTTPException(status_code=404, detail="User not found in Supabase")
    
    user_profile = supabase_res.data[0]

    # Fetch metrics from MongoDB
    recent_activities = list(activity_collection.find({"user_id": user_id}, {"_id": 0}).limit(10))
    screen_time_data = screen_time_collection.find_one({"user_id": user_id}, {"_id": 0})

    return {
        "profile": user_profile,
        "analytics": {
            "screen_time_summary": screen_time_data or {},
            "recent_activity_logs": recent_activities
        }
    }