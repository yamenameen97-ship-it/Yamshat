import datetime
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "SUPER_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    DATABASE_PATH = DATABASE_PATH
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
