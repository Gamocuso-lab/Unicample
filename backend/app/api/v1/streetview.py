from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from app.services.streetviewService import StreetviewService

load_dotenv()

router = APIRouter()

base_url = "/streetview"


@router.get("/streetview", response_class=HTMLResponse)
async def streetview(request: Request, location: str = None):

    api_key = os.getenv("STREET_VIEW_KEY")
    if not api_key:
        return HTMLResponse(content="<h1>Error: API key not found</h1>", status_code=500)
    
    service = StreetviewService()
    return service.get_streetview_image(location=location,key = api_key, request=request)
    

    