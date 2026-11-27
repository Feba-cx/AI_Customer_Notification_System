import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .preprocessing import create_customer_features
from .xgboost_model import create_xgboost_model


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "purchase_prediction_model.pkl"
)


def create_training_data():

    from models.customer import Customer
    from models.purchase_history import PurchaseHistory

    customers = Customer.query.all()

    data = []

    for customer in customers:

        purchases = (
            PurchaseHistory.query
            .filter_by(customer_id=customer.id)
            .order_by(PurchaseHistory.purchase_date)
            .all()
        )

        # Need at least 2 purchases
        if len(purchases) < 2:
            continue

        for i in range(len(purchases) - 1):

            current_purchase = purchases[i]
            next_purchase = purchases[i + 1]

            previous_purchases = purchases[:i + 1]

            purchase_count = len(previous_purchases)

            total_spent = sum(
                p.amount * p.quantity
                for p in previous_purchases
            )

            average_order_value = (
                total_spent / purchase_count
            )

            days_to_next_purchase = (
                next_purchase.purchase_date
                - current_purchase.purchase_date
            ).days

            # Target:
            # 1 = purchased again within 30 days
            # 0 = did not purchase again within 30 days

            will_purchase = (
                1 if days_to_next_purchase <= 30 else 0
            )

            data.append({

                "customer_id": customer.id,

                "purchase_count":
                    purchase_count,

                "total_spent":
                    total_spent,

                "average_order_value":
                    average_order_value,

                "days_since_last_purchase":
                    (
                        current_purchase.purchase_date
                        - purchases[0].purchase_date
                    ).days,

                "will_purchase":
                    will_purchase
            })

    return pd.DataFrame(data)


def train_purchase_model():

    df = create_training_data()

    if df.empty:
        print("No training data available.")
        return None

    if df["will_purchase"].nunique() < 2:
        print(
            "\nTraining stopped:"
            " the dataset contains only one target class."
        )
        print(
            "Add purchase-history records with"
            " different purchase dates."
        )
        return None

    features = [
        "purchase_count",
        "total_spent",
        "average_order_value",
        "days_since_last_purchase"
    ]

    X = df[features]
    y = df["will_purchase"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = create_xgboost_model()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"\nModel accuracy: {accuracy:.2f}"
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        f"Model saved to: {MODEL_PATH}"
    )

    return model