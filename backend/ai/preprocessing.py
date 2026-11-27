import pandas as pd
from datetime import date

from models.customer import Customer
from models.purchase_history import PurchaseHistory


def create_customer_features():

    customers = Customer.query.all()

    data = []

    today = date.today()

    for customer in customers:

        purchases = (
            PurchaseHistory.query
            .filter_by(customer_id=customer.id)
            .order_by(PurchaseHistory.purchase_date)
            .all()
        )

        purchase_count = len(purchases)

        # Calculate total spending from purchase history
        total_spent = sum(
            purchase.amount * purchase.quantity
            for purchase in purchases
        )

        # Calculate average order value
        average_order_value = (
            total_spent / purchase_count
            if purchase_count > 0
            else 0
        )

        # Calculate days since last purchase
        if purchases:

            last_purchase = purchases[-1].purchase_date

            days_since_last_purchase = (
                today - last_purchase
            ).days

        else:

            days_since_last_purchase = -1

        data.append({

            "customer_id": customer.id,

            "purchase_count":
                purchase_count,

            "total_spent":
                round(total_spent, 2),

            "average_order_value":
                round(average_order_value, 2),

            "days_since_last_purchase":
                days_since_last_purchase,

            "preferred_category":
                customer.preferred_category

        })

    return pd.DataFrame(data)