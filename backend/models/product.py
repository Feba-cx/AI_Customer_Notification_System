from database.database import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)