from __future__ import annotations

from ..src.server import load_model
from ..src.train_model import *

pipe = load_model()


def test_score():
    df = pd.read_csv(path_csv)
    train, test = model_selection.train_test_split(df)

    pred = pipe.predict(test[feature_columns])
    score = metrics.accuracy_score(test[target_column], pred)

    assert score > 0.6
