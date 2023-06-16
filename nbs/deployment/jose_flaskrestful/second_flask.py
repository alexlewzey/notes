"""Making a rest api with flask restful."""

from first_flask.db import db
from first_flask.resources import (Item, ItemList, Store, StoreList,
                                   UserRegister)
from first_flask.security import authenticate, identity
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///data.db"  # can change this to any sql database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "mole"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
