from fastapi.templating import Jinja2Templates
from app.utils.singleton import SingletonMeta

class StreetviewService(metaclass=SingletonMeta):

    def __init__(self):
        self.template = Jinja2Templates(directory="app/templates")

    def get_streetview_image(self, local=None, key=None, request=None, blur_level: int = 0):

        if not key:
            raise ValueError("API key is required")

        if not local:
            raise ValueError("Location is required")

        try:
            lat: float = local.split(",")[0] 
            lng: float = local.split(",")[1] 

        except (ValueError, IndexError):
            raise ValueError("Invalid location format. Please use 'lat,lng'.")

        return self.template.TemplateResponse("streetview.html", {
            "request": request,
            "google_maps_api_key": key,
            "lat": lat, 
            "lng": lng,
            "blur": blur_level 
        })