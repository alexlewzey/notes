from __future__ import annotations

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = "goonbay"

stores: list[dict[str, str | list]] = [
    {
        "name": "Pets at home",
        "items": ["chum", "tripe"],
    },
    {"name": "pets store", "items": ["backed beans"]},
    {
        "name": "eves gaff",
        "items": [
            "ridge",
            "chai seeds",
        ],
    },
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": [],
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message": "store not found"})


@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            item_new = {
                "name": request_data["name"],
                "price": request_data["price"],
            }
            store["items"].append(item_new)
            return jsonify(store)
    return jsonify({"message": f"invalid store name: {name}"})


@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": f"invalid store name: {name}"})


app.run(port=5000)
