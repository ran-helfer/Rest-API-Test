from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, UpdateItemSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/items")
class Items(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data) # should include the ItemModel data needed

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while trying to save")
        return item, 201

    @jwt_required(())
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # return {"items": list(items.values())}


@blp.route("/items/<int:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item


        #raise NotImplementedError("Getting store not implemented.")

        # try:
        #     return items[item_id]
        # except KeyError:
        #     return {"item Not found"}, 404

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted"}, 200

        # raise NotImplementedError("Delete item not implemented.")
        #
        # try:
        #     del items[item_id]
        #     return {"message" : "Item deleted"}, 201
        # except KeyError:
        #     return {"item Not found"}, 404

    @blp.response(200, ItemSchema)
    @blp.arguments(UpdateItemSchema)  # the data comes as first argument,
    # and using @blp also fix
    # swagger in case could not
    # enter body
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="bad request no name or price")
        #
        # try:
        #     current_item = items[item_id]
        #     item = { item_id : { **item_data, "id": item_id } }
        #     items.update(item)
        #     return item, 200
        # except KeyError:
        #     abort(404, message="Item not sound")
