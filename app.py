import uuid
import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
import models
import secrets
from flask_migrate import Migrate

from Resources.stores import blp as StoreBP
from Resources.items import blp as ItemsBP
from Resources.tag import blp as TagsBP
from Resources.user import blp as UsersBP
from blocklist import BLOCKLIST

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
    migrate = Migrate(app, db)
    api = Api(app)

    # Normally you would like to store a constant secret - since this means
    # that the secret will be changed each time the app is re run
    app.config["JWT_SECRET_KEY"] = "whatever"
    #app.secret_key = "whatever"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # TODO: Read from a config file instead of hard-coding
        if identity == 1: # identity is user number 1 as id
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # JWT configuration ends

    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    api.register_blueprint(StoreBP)
    api.register_blueprint(ItemsBP)
    api.register_blueprint(TagsBP)
    api.register_blueprint(UsersBP)

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
