from sqlalchemy import text

from app import db, create_app
from app.models import Store, Product, Shelf


def create_fts_index():
    # Create the full-text search index on the products table
    db.session.execute(
        text(
            """
    CREATE INDEX IF NOT EXISTS idx_fts_product_name 
    ON products USING gin(to_tsvector('english', name));
    """
        )
    )
    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        create_fts_index()

        print("Database tables created and full-text search index created")
