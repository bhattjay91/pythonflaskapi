import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import itemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = itemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if itemModel.find_by_name(name):
            return {"message": "An item with name '{}' already eists.".format(name)}, 400 #bad request

        data = Item.parser.parse_args()

        item = itemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message":"An error has occured when inserting the item."}, 500 #Internal Server Error

        return item.json(), 201

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = itemModel.find_by_name(name)

        if item is None:
            item = itemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':list(map(lambda x: x.json(), itemModel.query.all()))}
