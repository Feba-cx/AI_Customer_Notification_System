from database.database import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer
    )

    message = db.Column(
        db.Text
    )

    channel = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(30)
    )

    sent_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )