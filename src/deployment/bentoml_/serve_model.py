from __future__ import annotations

import bentoml
from bentoml._internal.runner.runner import Runner
from bentoml.io import NumpyNdarray

tag = bentoml.models.get("xgb_1")
runner: Runner = tag.to_runner()
service = bentoml.Service("xgb_classifier", runners=[runner])


@service.api(input=NumpyNdarray(shape=(1, 7)), output=NumpyNdarray())
def predict(data):
    label = runner.predict.run(data)
    return label
