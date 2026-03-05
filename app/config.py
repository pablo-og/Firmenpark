import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-firmenpark"
    SQLALCHEMY_DATABASE_URI = "sqlite:///firmenpark.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
