from first_flask.models.store import StoreModel
from flask_restful import Resource, reqparse


# noinspection PyMethodMayBeStatic
class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="this is required")

    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "invalid store"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "already exists"}, 401

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return {"message": "error happened while saving store"}
        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {"message": "store deleted"}
        return {"message": "store does not exist"}


# noinspection PyMethodMayBeStatic
class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
