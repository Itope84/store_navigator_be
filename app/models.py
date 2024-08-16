from dataclasses import dataclass
import uuid

from . import db


# Reference: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html


@dataclass
class Store(db.Model):
    id: uuid.UUID
    name: str
    address: str
    logo: str
    floor_plan: str

    @property
    def c_shelves(self):
        return [shelf.to_dict() for shelf in self.shelves]

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "address": self.address,
            "logo": self.logo,
            "floor_plan": self.floor_plan,
            "shelves": self.c_shelves,
        }

    __tablename__ = "stores"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=True)
    floor_plan = db.Column(db.String(200), nullable=True)
    shelves = db.relationship("Shelf", back_populates="store", lazy=True)


product_shelves = db.Table(
    "product_shelves",
    db.Column("product_id", db.ForeignKey("products.id"), primary_key=True),
    db.Column("shelf_id", db.ForeignKey("shelves.id"), primary_key=True),
)


@dataclass
class Product(db.Model):
    id: uuid.UUID
    name: str
    price: float
    description: str
    image: str

    __tablename__ = "products"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)
    shelves = db.relationship(
        "Shelf", secondary=product_shelves, back_populates="products", lazy=True
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
        }


@dataclass
class Shelf(db.Model):
    id: uuid.UUID
    subcategory_name: str
    section: str
    store_id: uuid.UUID
    description: str
    shelf_number: str

    __tablename__ = "shelves"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subcategory_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(100), nullable=False)
    store_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("stores.id"), nullable=False
    )
    description = db.Column(db.String(1000), nullable=True)
    shelf_number = db.Column(db.String(100), nullable=False)
    products = db.relationship(
        "Product", secondary=product_shelves, back_populates="shelves"
    )
    store = db.relationship("Store", back_populates="shelves", lazy=True)

    @property
    def map_node_id(self) -> str:
        return f"section_{self.shelf_number}"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.subcategory_name,
            "section": self.section,
            "store_id": str(self.store_id),
            "description": self.description,
            "map_node_id": self.map_node_id,
        }
