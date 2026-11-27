from models.notification import Notification
from database.database import db


def generate_sales_message(
    customer_name,
    product_name,
    price,
    purchase_intent
):

    if purchase_intent == "High":
        message = (
            f"Hi {customer_name}! "
            f"We think you'll love our {product_name}. "
            f"It's available now for ₹{price:.0f}. "
            f"Check it out before it's gone!"
        )

    elif purchase_intent == "Medium":
        message = (
            f"Hi {customer_name}! "
            f"We found something you may like — "
            f"{product_name}, available for ₹{price:.0f}. "
            f"Take a look when you have a moment!"
        )

    else:
        message = (
            f"Hi {customer_name}! "
            f"Discover our {product_name}, "
            f"now available for ₹{price:.0f}. "
            f"Have a look and see if it's right for you!"
        )

    return message


def save_notification(
    customer_id,
    message,
    channel="dashboard"
):

    notification = Notification(
        customer_id=customer_id,
        message=message,
        channel=channel,
        status="Generated"
    )

    db.session.add(notification)
    db.session.commit()

    return notification