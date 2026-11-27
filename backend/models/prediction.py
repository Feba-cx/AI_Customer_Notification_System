from database.database import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id")
    )

    purchase_probability = db.Column(db.Float)

    purchase_intent = db.Column(
        db.String(50)
    )

    recommended_product = db.Column(
        db.String(150)
    )