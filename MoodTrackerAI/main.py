from fastapi import FastAPI
from routes.users import router as user_router
from routes.analytics import router as analytics_router

app = FastAPI(
    title="MoodTrackerAI Hybrid Backend",
    description="Hybrid Supabase + MongoDB Surveillance & Behavioral Engine",
    version="1.0.0"
)

# Register Routers
app.include_router(user_router)
app.include_router(analytics_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "online", "message": "Hybrid Supabase + MongoDB System Active"}