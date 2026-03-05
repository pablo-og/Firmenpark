from flask import Blueprint

bp = Blueprint("invoice", __name__, url_prefix="/invoice")

from app.blueprints.invoice import routes  # noqa: E402
