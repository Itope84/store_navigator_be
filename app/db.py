from . import db, create_app
from models import Store, Product, Shelf

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
