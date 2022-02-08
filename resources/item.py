from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # use the parser to parse the request
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be empty")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store_id")

    # the parser going to put the "valid" fields in the data, the arguments that we defined

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': f'An error occurred retrieving item {name}'}, 500
        if item is None:
            return {'message': 'Item not found'},404
        return item.json()

    @jwt_required()
    def post(self, name):
        # check if there is already item with this name
        if ItemModel.find_by_name(name):
            return {'message': f'Item {name} already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
           item.save_to_db()
        except:
            return {'message': f'An error occurred inserting item {name}'}, 500

        # 201 is status code for created
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': f'item {name} deleted successfully'}

    @jwt_required()
    def put(self, name):
        #old version to get json payload, data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class Items(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.query.all()
        return {"items": [item.json() for item in items]}
        # or return {"items": list(map(lambda x: x.json(), ItemModel.query.all())}