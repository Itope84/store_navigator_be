# create a new store
from app import db, create_app
import json
import pandas as pd
from app.models import Store, Shelf, Product

new_store = Store(
    name="Tesco",
    address="123 Market St",
    logo="http://example.com/logo.png",
    floor_plan="floor_plan.svg",
)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.session.add(new_store)
        db.session.commit()

        stores = Store.query.all()

        store = stores[0]

        with open("app/category_sections.json") as f:
            data = json.load(f)

        for section in data:
            shelf = Shelf(
                subcategory_name=section["category"],
                section=section["division"],
                shelf_number=section["shelf"],
                store_id=store.id,
            )

            db.session.add(shelf)
        db.session.commit()

        shelves = Shelf.query.all()

        shelf_map = {shelf.subcategory_name: shelf.id for shelf in shelves}

        data = pd.read_csv("app/tesco_groceries_dataset.csv")

        for index, row in data.iterrows():
            shelf_name = row["breadcrumbs"].split("~")[-2]
            shelf_id = shelf_map[shelf_name]

            shelf = Shelf.query.get(shelf_id)

            p = Product(
                name=row["name"], price=row["price"], image=row["images"].split("~")[0]
            )

            p.shelves.append(Shelf.query.get(shelf_id))
            db.session.add(p)

        db.session.commit()
        print("products seeded")

        shelves = Shelf.query.all()
        products = shelves[0].products
        print(products[0].name)
