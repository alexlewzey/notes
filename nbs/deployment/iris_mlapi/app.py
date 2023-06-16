"""Restful api that can classify a flower with a pre-trained tensorflow model."""
import json
import logging

import numpy as np
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from tensorflow.keras.models import load_model

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("sepal_length", type=float)
parser.add_argument("sepal_width", type=float)
parser.add_argument("petal_length", type=float)
parser.add_argument("petal_width", type=float)

with open("mapping.json") as f:
    mapping = json.load(f)
    mapping = {int(i): nm for i, nm in mapping.items()}

model = load_model("flower_classifier")


class PredictSpecies(Resource):
    def get(self):
        print("making get request")

        args = parser.parse_args()
        sepal_length = args["sepal_length"]
        sepal_width = args["sepal_width"]
        petal_length = args["petal_length"]
        petal_width = args["petal_width"]

        obvs = np.array(
            [
                [
                    sepal_length,
                    sepal_width,
                    petal_length,
                    petal_width,
                ]
            ]
        )
        pred = model.predict(obvs).flatten()
        print(f"mapping: {mapping}")
        print(f"pred: {pred}")
        pred_nm = mapping[pred.argmax()]
        return jsonify({"message": f"it's at {pred_nm}"})


api.add_resource(PredictSpecies, "/predict/flower")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
