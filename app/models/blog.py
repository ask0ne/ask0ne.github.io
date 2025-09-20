from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    date: str
    slug: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample Blog Post",
                "content": "This is a sample blog post content.",
                "slug": "sample-blog-post"
            }
        }

class BlogPostCreate(BaseModel):
    title: str
    content: str

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None