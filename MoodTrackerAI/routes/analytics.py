from fastapi import APIRouter
from datetime import datetime
from database.mongo_client import activity_collection, screen_time_collection
from models.activity_models import ActivityLogCreate

router = APIRouter(prefix="/analytics", tags=["Analytics (MongoDB)"])

@router.post("/log-activity")
def log_activity(activity: ActivityLogCreate):
    activity_doc = activity.dict()
    activity_doc["timestamp"] = datetime.utcnow()

    # Basic Sentiment / Mood Logic
    detected_mood = "neutral"
    if activity.video_category == "sad" and activity.watch_time_seconds > 10:
        detected_mood = "sad"
    elif activity.video_category == "comedy" and activity.watch_time_seconds > 10:
        detected_mood = "happy"

    activity_doc["detected_mood"] = detected_mood
    activity_collection.insert_one(activity_doc)

    # Upsert screen time summary
    screen_time_collection.update_one(
        {"user_id": activity.user_id},
        {
            "$inc": {"total_screen_time_seconds": activity.watch_time_seconds},
            "$set": {"last_active": datetime.utcnow()}
        },
        upsert=True
    )

    return {"status": "Logged to MongoDB", "detected_mood": detected_mood}