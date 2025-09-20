from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def create_app() -> FastAPI:
    app = FastAPI(title="atharva")
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    return app

# Templates configuration
templates = Jinja2Templates(directory="templates")