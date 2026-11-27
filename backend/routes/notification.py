
from flask import Blueprint, jsonify, render_template

from ai.notification_pipeline import generate_customer_notification
from models.customer import Customer


notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/notifications"
)


# ======================================================
# NOTIFICATIONS PAGE
# ======================================================

@notification_bp.route("/", methods=["GET"])
def notifications_page():

    return render_template("notification.html")


# ======================================================
# GENERATE AI NOTIFICATIONS
# ======================================================

@notification_bp.route(
    "/generate",
    methods=["GET"]
)
def generate_notifications():

    customers = Customer.query.all()

    results = []

    for customer in customers:

        result = generate_customer_notification(
            customer.id
        )

        if result:
            results.append(result)

    return jsonify({
        "success": True,
        "count": len(results),
        "notifications": results
    })


# ======================================================
# GET SAVED NOTIFICATIONS
# ======================================================

@notification_bp.route(
    "/list",
    methods=["GET"]
)
def list_notifications():

    from models.notification import Notification
    from models.prediction import Prediction
    from models.product import Product

    notifications = (
        Notification.query
        .order_by(
            Notification.sent_at.desc()
        )
        .all()
    )

    results = []

    for notification in notifications:

        customer = Customer.query.get(
            notification.customer_id
        )

        prediction = (
            Prediction.query
            .filter_by(
                customer_id=notification.customer_id
            )
            .order_by(
                Prediction.id.desc()
            )
            .first()
        )

        product = None

        if prediction and prediction.recommended_product:

            product = (
                Product.query
                .filter_by(
                    product_name=
                    prediction.recommended_product
                )
                .first()
            )

        results.append({

            "id":
                notification.id,

            "customer_id":
                notification.customer_id,

            "customer_name":
                customer.name
                if customer
                else "Unknown",

            "message":
                notification.message,

            "channel":
                notification.channel,

            "status":
                notification.status,

            "sent_at":
                notification.sent_at.isoformat()
                if notification.sent_at
                else None,

            "purchase_probability":
                prediction.purchase_probability
                if prediction
                else 0,

            "purchase_intent":
                prediction.purchase_intent
                if prediction
                else "Unknown",

            "recommended_product":
                prediction.recommended_product
                if prediction
                else "None",

            "price":
                float(product.price)
                if product
                else 0

        })

    return jsonify({

        "success": True,

        "count":
            len(results),

        "notifications":
            results

    })

