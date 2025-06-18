from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.singleton import SingletonMeta

class StreetviewService(metaclass=SingletonMeta):

    def __init__(self):
        self.template = Jinja2Templates(directory="app/templates")

    def get_streetview_image(self, location = None, key=None, request=None):

        if not key:
            return ValueError("API key is required")

        if not location:
            return ValueError("Location is required")

        try:
            lat: float = location.split(",")[0] 
            lng: float = location.split(",")[1] 

        except (ValueError, IndexError):
            return ValueError("Invalid location format. Please use 'lat,lng'.")

        return self.template.TemplateResponse("streetview.html", {
            "request": request,
            "google_maps_api_key": key,
            "lat": lat, 
            "lng": lng
        })
