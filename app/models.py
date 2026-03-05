from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ICSEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20))
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
