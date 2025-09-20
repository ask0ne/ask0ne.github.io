from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.core.config import templates
from app.db.blog import BlogDatabase

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/section/{section_id}", response_class=HTMLResponse)
async def get_section(request: Request, section_id: str):
    section_templates = {
        "me": "sections/me.html",
        "cv": "sections/cv.html",
        "scribblings": "sections/scribblings.html",
        "mystery": "sections/mystery.html"
    }

    template = section_templates.get(section_id)
    if not template:
        raise HTTPException(status_code=404, detail="Section not found")

    context = {"request": request, "section_id": section_id}

    if section_id == "scribblings":
        context["posts"] = BlogDatabase.get_all_posts()

    return templates.TemplateResponse(template, context)