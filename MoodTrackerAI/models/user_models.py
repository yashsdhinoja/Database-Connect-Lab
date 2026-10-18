from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserProfileCreate(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    age: int

class UserProfileResponse(UserProfileCreate):
    no_posts: int = 0 
    no_videos: int = 0
    followers_count: int = 0
    following_count:int = 0 