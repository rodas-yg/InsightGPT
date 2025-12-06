import os

# Holds configuration settings for the Flask app.
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = "AIzaSyAWWr8jaAAA2jVkcM8Su4NbGdTQlLuEfno" 

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
