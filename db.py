from app import db, app
from models import Store, Product, Shelf, ProductShelf

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
