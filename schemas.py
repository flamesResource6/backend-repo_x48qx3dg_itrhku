"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class Video(BaseModel):
    """
    Streaming videos collection schema
    Collection name: "video"
    """
    title: str = Field(..., description="Video title")
    description: Optional[str] = Field(None, description="Short description")
    thumbnail: Optional[HttpUrl] = Field(None, description="Thumbnail image URL")
    source: HttpUrl = Field(..., description="MP4/HLS source URL")
    duration: Optional[int] = Field(None, ge=0, description="Duration in seconds")
    category: Optional[str] = Field(None, description="Category or tag")

class Training(BaseModel):
    """
    Training lessons collection schema
    Collection name: "training"
    """
    title: str = Field(..., description="Lesson title")
    summary: Optional[str] = Field(None, description="Brief summary")
    steps: Optional[List[str]] = Field(default_factory=list, description="Step-by-step guidance")
    video_id: Optional[str] = Field(None, description="Related video id (string)")

# Example additional schemas can be added below as needed.
