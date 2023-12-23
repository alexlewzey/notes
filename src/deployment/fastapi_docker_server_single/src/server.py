from __future__ import annotations

import pickle
from pathlib import Path

import fastapi
import pandas as pd
import pydantic

root = Path(__file__).parent
path_model = root.parent / "model" / "classifier.pkl"

app = fastapi.FastAPI(title="penguin prediction service")


class Penguin(pydantic.BaseModel):
    island: str
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    sex: str
    year: int


def load_model():
    with path_model.open("rb") as f:
        pipe = pickle.load(f)
    return pipe


@app.get("/")
def home():
    return (
        "Congratulations your api is working. Head over to http://www.localhost:80/docs"
    )


@app.post("/predict")
def predict(penguin: Penguin):
    data_point = pd.DataFrame([penguin.dict()])
    pred = pipe.predict(data_point)
    body = {"prediction": pred.tolist()[0]}
    print(body)
    return body


pipe = load_model()
