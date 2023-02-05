import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel, ItemModel
from schemas import PlainStoreSchema, StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

#        try:
#            return stores[store_id]
#        except KeyError:
#           abort(404, message="Store Not found")

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        #print("Check this Ran:")
        #print(store.items)
        #print(store.items)
        #if store.items != None:
        #    return {"message" : "store has items, please delete items before deleting a store"}, 403

        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}
        # try:
        #     del stores[store_id]
        #     return {"message" : "Store Deleted"}
        # except KeyError:
        #     abort(404, message="Not found")


@blp.route("/stores")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
        #raise NotImplementedError("Getting stores not implemented.")
        #return {"stores": list(stores.values())}

    @blp.arguments(PlainStoreSchema)
    @blp.response(200, PlainStoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)  # should include the ItemModel data needed

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with such name exist")
        except SQLAlchemyError:
            abort(500, message="An error occured while trying to save a store")
        return store, 201
