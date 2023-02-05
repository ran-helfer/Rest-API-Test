import uuid
import os
from flask import Flask
from flask_smorest import Api

from db import db
import models

from Resources.stores import blp as StoreBP
from Resources.items import blp as ItemsBP
from Resources.tag import blp as TagsBP

# create_app function is the application factory function
def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBP)
    api.register_blueprint(ItemsBP)
    api.register_blueprint(TagsBP)

    return app





# if __name__ == '__main__':
#     app.run(port=5001)
#
#
# # @app.get("/stores")
# # def get_stores():
# #     return {"stores": list(stores.values())}
# #
# # @app.post("/store")
# # def create_store():
# #     store_data = request.get_json()
# #     store_id = uuid.uuid4().hex
# #     new_store = { **store_data, "id": store_id }
# #     stores[store_id] = new_store
# #     return new_store, 201
#
#
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     if (
#         "price" not in item_data
#         or "name" not in item_data
#     ):
#             abort(400, message="Bad request, need to specify item price and item name")
#
#     # if item_data["store_id"] not in stores:
#     #     return  {"message" : "store not found"}, 404
#
#     item_id = uuid.uuid4().hex
#     item = { **item_data, "id" : item_id}
#     items[item_id] = item
#     return item, 201
#
#
# @app.get("/items")
# def get_all_items():
#     return {"items": list(items.values())}
#
# # @app.get("/store/<string:store_id>")
# # def get_store(store_id):
# #     try:
# #         return stores[store_id]
# #     except KeyError:
# #         abort(404, message="Store Not found")
#
#
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         return {"item Not found"}, 404
#
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#       del items[item_id]
#       return {"message" : "Item deleted"}, 201
#     except KeyError:
#         return {"item Not found"}, 404
#
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(400, message="bad request no name or price")
#
#     try:
#         current_item = items[item_id]
#         item = { item_id : { **item_data, "id": item_id } }
#         items.update(item)
#         return item, 200
#     except KeyError:
#         abort(404, message="Item not sound")
#
