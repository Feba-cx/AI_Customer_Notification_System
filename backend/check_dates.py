from datetime import date

from app import app
from models.customer import Customer
from models.purchase_history import PurchaseHistory


with app.app_context():

    print("Today:", date.today())
    print()

    customers = Customer.query.all()

    for customer in customers:

        purchases = (
            PurchaseHistory.query
            .filter_by(customer_id=customer.id)
            .order_by(PurchaseHistory.purchase_date)
            .all()
        )

        if purchases:
            print(
                customer.name,
                "-> Last purchase:",
                purchases[-1].purchase_date
            )