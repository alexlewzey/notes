from __future__ import annotations

import pickle
from pathlib import Path

import lightgbm as lgb
import pandas as pd
from sklearn import compose, metrics, model_selection, pipeline, preprocessing

root = Path(__file__).parent
path_model = root.parent / "model" / "classifier.pkl"

path_csv = root.parent / "data" / "penguins.csv"
df = pd.read_csv(path_csv)

category_columns = ["island", "sex", "year"]
continuous_columns = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]
feature_columns = category_columns + continuous_columns
target_column = "species"

if __name__ == "__main__":
    category_transformer = pipeline.Pipeline(
        [("encoder", preprocessing.OrdinalEncoder())]
    )

    transformer = compose.ColumnTransformer(
        [
            ("category_transformer", preprocessing.OrdinalEncoder(), category_columns),
        ]
    )

    pipe = pipeline.Pipeline(
        [
            ("transformer", transformer),
            ("classify", lgb.LGBMClassifier()),
        ]
    )

    train, test = model_selection.train_test_split(df)
    train["train"] = "train"
    test["test"] = "test"

    pipe.fit(train[feature_columns], train[target_column])
    train["y_pred"] = pipe.predict(train[feature_columns])
    train["y_prob"] = pipe.predict_proba(train[feature_columns])[:, -1]

    test["y_pred"] = pipe.predict(test[feature_columns])
    test["y_prob"] = pipe.predict_proba(test[feature_columns])[:, -1]

    scores = {
        "train": {
            "accuracy": metrics.accuracy_score(train[target_column], train["y_pred"]),
            "f1": metrics.f1_score(
                train[target_column], train["y_pred"], average="micro"
            ),
        },
        "test": {
            "accuracy": metrics.accuracy_score(test[target_column], test["y_pred"]),
            "f1": metrics.f1_score(
                test[target_column], test["y_pred"], average="micro"
            ),
        },
    }

    with path_model.open("wb") as f:
        pickle.dump(pipe, f)

    print(f"script complete saved model: {path_model.as_posix()}")
