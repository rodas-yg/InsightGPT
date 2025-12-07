import os
from dotenv import load_dotenv# Holds configuration settings for the Flask app.
class Config:
    load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = API_KEY 

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
