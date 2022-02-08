from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    # use the parser to parse the request
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be empty")

    @jwt_required()
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return { 'message': 'An error occurred accessing db'}
        if store is None:
            return {'message': 'store not found'}, 404
        return store.json()

    @jwt_required()
    def post(self, name):
        # check if there is already store with this name
        try:
            if StoreModel.find_by_name(name):
                return {'message': f'store {name} already exists'}, 400
        except:
            return { 'message': 'An error occurred accessing db'}

        store = StoreModel(name)

        try:
           store.save_to_db()
        except:
            return {'message': f'An error occurred inserting store {name}'}, 500

        # 201 is status code for created
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': f'store {name} deleted successfully'}

class StoreList(Resource):

    @jwt_required()
    def get(self):
        stores = StoreModel.query.all()
        return {"store": [store.json() for store in stores]}