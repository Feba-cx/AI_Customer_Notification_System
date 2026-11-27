from models.prediction import Prediction
from database.database import db


def save_prediction(
    customer_id,
    purchase_probability,
    purchase_intent,
    recommended_product
):
    prediction = Prediction(
        customer_id=customer_id,
        purchase_probability=purchase_probability,
        purchase_intent=purchase_intent,
        recommended_product=recommended_product
    )

    db.session.add(prediction)
    db.session.commit()

    return prediction