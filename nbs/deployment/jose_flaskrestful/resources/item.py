from first_flask.models import ItemModel
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


# noinspection PyMethodMayBeStatic
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        """Get item from database."""
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "item does not exist"}, 404

    def post(self, name: str):
        """Insert item to database if it does not already exist."""
        if Item.find_by_name(name):
            return {"message": f"item already exists: {name}"}, 401

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception:
            return {"message": f"error while trying to insert {name}"}, 500
        return item.json(), 201

    def delete(self, name):
        """Delete item if it does not already exist."""
        item = ItemModel.find_by_name(name)
        if item:
            item.delete(name)

    def put(self, name):
        """Can be used to create or update, idempotent, the result should be independent
        of previous results."""
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json(), 201


# noinspection PyMethodMayBeStatic
class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
