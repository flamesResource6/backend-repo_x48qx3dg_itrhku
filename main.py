import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI(title="Beb Stream API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic response models
class VideoOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    source: str
    duration: Optional[int] = None
    category: Optional[str] = None

class TrainingOut(BaseModel):
    id: str
    title: str
    summary: Optional[str] = None
    steps: List[str] = []
    video_id: Optional[str] = None

@app.get("/")
def root():
    return {"name": "Beb Streaming Backend", "status": "ok"}

@app.get("/api/videos", response_model=List[VideoOut])
def list_videos():
    try:
        docs = get_documents("video")
        results = []
        for d in docs:
            results.append(VideoOut(
                id=str(d.get("_id")),
                title=d.get("title", "Untitled"),
                description=d.get("description"),
                thumbnail=d.get("thumbnail"),
                source=d.get("source"),
                duration=d.get("duration"),
                category=d.get("category"),
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trainings", response_model=List[TrainingOut])
def list_trainings():
    try:
        docs = get_documents("training")
        results = []
        for d in docs:
            results.append(TrainingOut(
                id=str(d.get("_id")),
                title=d.get("title", "Untitled"),
                summary=d.get("summary"),
                steps=d.get("steps", []) or [],
                video_id=str(d.get("video_id")) if d.get("video_id") else None,
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seed endpoint to add demo content if database is empty
@app.post("/api/seed")
def seed_content():
    try:
        # Check if videos exist
        existing_videos = get_documents("video", limit=1)
        if not existing_videos:
            demo_videos = [
                {
                    "title": "Beb: Welcome to the Playground",
                    "description": "A vibrant intro with playful shapes and upbeat vibes.",
                    "thumbnail": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=1200&auto=format&fit=crop",
                    "source": "https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-720p.mp4",
                    "duration": 52,
                    "category": "intro"
                },
                {
                    "title": "Beb Training: Quick Start",
                    "description": "Learn the basics in minutes with animated guidance.",
                    "thumbnail": "https://images.unsplash.com/photo-1529336953121-ad3c78a6b8b7?q=80&w=1200&auto=format&fit=crop",
                    "source": "https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-1080p.mp4",
                    "duration": 68,
                    "category": "training"
                }
            ]
            for v in demo_videos:
                create_document("video", v)
        
        existing_trainings = get_documents("training", limit=1)
        if not existing_trainings:
            demo_trainings = [
                {
                    "title": "Getting Started",
                    "summary": "Understand navigation, playback, and progress.",
                    "steps": [
                        "Open the app and explore the neon hero.",
                        "Pick a video from the carousel.",
                        "Use keyboard or on-screen controls to play/pause.",
                        "Track your progress in the Training tab."
                    ]
                },
                {
                    "title": "Pro Tips",
                    "summary": "Speed, quality, and hidden shortcuts.",
                    "steps": [
                        "Press J/K/L for quick seek.",
                        "Use gear icon to adjust quality.",
                        "Hit F for fullscreen magic.",
                    ]
                }
            ]
            for t in demo_trainings:
                create_document("training", t)
        
        return {"status": "seeded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
