import uvicorn
from app.core.config import create_app
from app.routes import blog, sections

app = create_app()

# Include routers
app.include_router(sections.router)
app.include_router(blog.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
