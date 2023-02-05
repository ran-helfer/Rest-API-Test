from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    # name is unique for all stores, if we want unique tag per store
    # and not globally we would need to deal this differently
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")

    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")