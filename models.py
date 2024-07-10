import uuid
from app import db


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=True)
    floor_plan = db.Column(db.String(200), nullable=True)
    shelves = db.relationship("Shelf", backref="store", lazy=True)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    shelves = db.relationship("ProductShelf", back_populates="product")


class Shelf(db.Model):
    __tablename__ = "shelves"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subcategory_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(100), nullable=False)
    store_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("stores.id"), nullable=False
    )
    description = db.Column(db.String(200), nullable=True)
    shelf_number = db.Column(db.String(100), nullable=False)
    products = db.relationship("ProductShelf", back_populates="shelf")


class ProductShelf(db.Model):
    __tablename__ = "product_shelf"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("products.id"), primary_key=True
    )
    shelf_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("shelves.id"), primary_key=True
    )
    product = db.relationship("Product", back_populates="shelves")
    shelf = db.relationship("Shelf", back_populates="products")
