import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Unicample"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()