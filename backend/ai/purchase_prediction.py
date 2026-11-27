import os
import joblib

from .preprocessing import create_customer_features


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "purchase_prediction_model.pkl"
)


def predict_customer_purchase(customer_id):

    # Check whether trained model exists
    if not os.path.exists(MODEL_PATH):
        print("Purchase prediction model not found.")
        return None

    # Load trained XGBoost model
    model = joblib.load(MODEL_PATH)

    # Get customer features
    df = create_customer_features()

    # Find requested customer
    customer_data = df[
        df["customer_id"] == customer_id
    ]

    if customer_data.empty:
        print(
            f"Customer {customer_id} not found."
        )
        return None

    # Features used during training
    features = [
        "purchase_count",
        "total_spent",
        "average_order_value",
        "days_since_last_purchase"
    ]

    X = customer_data[features]

    # Predict probability
    probability = model.predict_proba(X)[0][1]

    # Convert probability into intent
    if probability >= 0.70:
        purchase_intent = "High"

    elif probability >= 0.40:
        purchase_intent = "Medium"

    else:
        purchase_intent = "Low"

    return {
        "customer_id": customer_id,
        "purchase_probability": round(
            float(probability),
            4
        ),
        "purchase_intent": purchase_intent
    }