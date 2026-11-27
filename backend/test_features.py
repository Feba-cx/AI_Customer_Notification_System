from app import app
from ai.preprocessing import create_customer_features


with app.app_context():

    df = create_customer_features()

    print("\nCUSTOMER FEATURES:")
    print(df)

    print("\nCOLUMNS:")
    print(df.columns.tolist())