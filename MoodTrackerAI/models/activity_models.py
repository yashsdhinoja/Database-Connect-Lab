from pydantic import BaseModel
from typing import Optional

class ActivityLogCreate(BaseModel):
    user_id: str
    video_id: str
    video_category: str  # e.g., "sad", "comedy", "motivational"
    watch_time_seconds: int
    interaction: str      # e.g., "like", "skip", "comment"
    screen_time_session: int  # in minutes