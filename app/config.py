import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-firmenpark"
    SQLALCHEMY_DATABASE_URI = "sqlite:///firmenpark.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SITE_NAME = os.environ.get("SITE_NAME", "Firmenpark.net")
    SITE_EMAIL = os.environ.get("SITE_EMAIL", "info@firmenpark.net")
    SITE_NAME_LEGAL = os.environ.get("SITE_NAME_LEGAL", "Firmenpark.net")
    SITE_STREET = os.environ.get("SITE_STREET", "")
    SITE_ZIP = os.environ.get("SITE_ZIP", "")
    SITE_CITY = os.environ.get("SITE_CITY", "")
