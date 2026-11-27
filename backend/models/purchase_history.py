from database.database import db


class PurchaseHistory(db.Model):

    __tablename__ = "purchase_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    product_name = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    purchase_date = db.Column(
        db.Date,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )