from ai.purchase_prediction import predict_customer_purchase
from ai.recommendation import recommend_product
from ai.message_generator import generate_sales_message, save_notification
from models.customer import Customer


def generate_customer_notification(customer_id):

    # 1. Predict purchase intent
    prediction = predict_customer_purchase(customer_id)

    if prediction is None:
        return None

    # 2. Recommend a product
    recommendation = recommend_product(customer_id)

    if recommendation is None:
        return None

    # 3. Get customer information
    customer = Customer.query.get(customer_id)

    if customer is None:
        return None

    # 4. Generate personalized message
    message = generate_sales_message(
        customer.name,
        recommendation["product_name"],
        recommendation["price"],
        prediction["purchase_intent"]
    )

    # 5. Save notification
    notification = save_notification(
        customer_id,
        message,
        "dashboard"
    )

    return {
        "customer_id": customer_id,
        "customer_name": customer.name,
        "purchase_probability": prediction[
            "purchase_probability"
        ],
        "purchase_intent": prediction[
            "purchase_intent"
        ],
        "recommended_product": recommendation[
            "product_name"
        ],
        "price": recommendation["price"],
        "message": message,
        "notification_id": notification.id
    }