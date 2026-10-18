from fastapi import APIRouter, HTTPException
from database.supabase_client import supabase
from models.user_models import UserProfileCreate

router = APIRouter(prefix="/users", tags=["Users (Supabase)"])


@router.post("/create")
def create_user_profile(profile: UserProfileCreate):
    try:
        # Pydantic v2 syntax: model_dump() instead of dict()
        response = (
            supabase.table("profiles").insert(profile.model_dump()).execute()
        )
        return {"status": "User created in Supabase", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}")
def get_user_profile(user_id: str):
    response = (
        supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]