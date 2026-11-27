import pandas as pd


def prepare_features(df):

    if df.empty:
        return df

    features = df.copy()

    # Convert category into numerical representation
    features = pd.get_dummies(
        features,
        columns=["preferred_category"],
        dtype=int
    )

    return features