from database.database import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20))

    city = db.Column(db.String(100))

    age = db.Column(db.Integer)

    purchase_history = db.Column(db.Text)

    preferred_category = db.Column(db.String(100))

    total_spent = db.Column(db.Float, default=0)