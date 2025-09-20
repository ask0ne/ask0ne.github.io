from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.core.config import templates
from app.db.blog import BlogDatabase
from app.models.blog import BlogPost, BlogPostCreate

router = APIRouter()

@router.get("/blog", response_class=HTMLResponse)
async def get_blog_list(request: Request):
    return templates.TemplateResponse("blog/list.html", {
        "request": request, 
        "posts": BlogDatabase.get_all_posts()
    })

@router.get("/blog/{post_id}", response_class=HTMLResponse)
async def get_blog_post(request: Request, post_id: int):
    post = BlogDatabase.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse("blog/detail.html", {
        "request": request,
        "post": post
    })

@router.post("/blog", response_class=HTMLResponse)
async def create_blog_post(request: Request, title: str = Form(...), content: str = Form(...)):
    slug = title.lower().replace(" ", "-").replace("'", "")
    new_post = BlogPost(
        title=title,
        content=content,
        date=datetime.now().strftime("%Y-%m-%d"),
        slug=slug
    )
    created_post = BlogDatabase.create_post(new_post)
    return templates.TemplateResponse("blog/detail.html", {
        "request": request,
        "post": created_post
    })