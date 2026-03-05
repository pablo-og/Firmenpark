from flask import Flask
from app.config import Config
from app.models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.blueprints.main import bp as main_bp
    from app.blueprints.invoice import bp as invoice_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(invoice_bp)

    with app.app_context():
        db.create_all()

    return app
