from flask import jsonify, request, Flask
from sqlalchemy import and_
from urllib.parse import unquote_plus

from app.search import bulk_search_products

from .models import Product, Shelf, Store
from .route_generation import FloorplanGrid, svg_to_ndarray


def init_routes(app: Flask):
    @app.route("/stores", methods=["GET"])
    def get_stores():
        stores = Store.query.all()
        return jsonify([store.to_dict() for store in stores])

    @app.route("/stores/<store_id>/shelves", methods=["GET"])
    def get_shelves(store_id):
        store: Store = Store.query.get(store_id)
        shelves = store.shelves
        return jsonify([shelf.to_dict() for shelf in shelves])

    @app.route("/products", methods=["GET"])
    def get_products():
        # search
        search = request.args.get("search")
        ids = request.args.get("ids")
        if ids:
            ids = ids.split(",")
            products = Product.query.filter(Product.id.in_(ids)).all()
        elif search:
            products = Product.query.filter(Product.name.ilike(f"%{search}%")).all()
        else:
            # no need to paginate for now. There's like 500+ results, the mobile app can handle the scrolling with a list builder
            # Include product.store in the response
            products = Product.query.all()

        return jsonify(products)

    @app.route("/products/bulk-search", methods=["GET"])
    def products_multiline_search():
        raw_queries = request.args.get("query", "")

        if raw_queries:
            decoded_queries = unquote_plus(raw_queries)

            print(decoded_queries)

            # find all \n in decoded_queries
            # has_newline = decoded_queries.find("\n") != -1
            # print("has newline", has_newline)

            # # Split by both URL-encoded (%0A) and regular newlines
            # queries = decoded_queries.replace("%0A", "\n")
            # print(queries)
            queries = decoded_queries.split("\n")

            print(queries)

            queries = [q.strip() for q in queries if q.strip()]

            if queries:
                results = bulk_search_products(queries)
                return jsonify(results)

        return jsonify({})

    @app.route("/stores/<store_id>/product-shelves", methods=["GET"])
    def get_product_shelves(store_id):
        store: Store = Store.query.get(store_id)
        # we need to fetch the shelves for given list of products
        product_ids = request.args.get("products")
        if product_ids:
            product_ids = product_ids.split(",")
            products = (
                Product.query.join(Product.shelves)
                .filter(and_(Product.id.in_(product_ids), Shelf.store_id == store_id))
                .all()
            )

            products_dict = [
                {
                    "product": product.to_dict(),
                    "section_id": (
                        product.shelves[0].map_node_id if product.shelves else None
                    ),
                }
                for product in products
            ]

            return jsonify(products_dict)
        else:
            return jsonify([])

    @app.route("/get-traveling-routes", methods=["GET"])
    def get_store_route():
        start = request.args.get("start") or "section_entrance"
        section_ids = request.args.get("section_ids")

        if not section_ids:
            return jsonify([])

        # TODO: get the store's map from the database
        floorplan = FloorplanGrid("app/floor_plan.svg")

        route = floorplan.get_optimal_routes(start, section_ids.split(","))

        return jsonify(route)

    @app.route("/get-route", methods=["GET"])
    def get_route():
        start = request.args.get("start")
        end = request.args.get("end")

        floorplan = FloorplanGrid("app/floor_plan.svg")

        route = floorplan.get_route(start, end)

        return jsonify(route)

    @app.route("/get-grid", methods=["GET"])
    def get_grid():
        grid = svg_to_ndarray("app/floor_plan_mini.svg")

        return jsonify(grid.tolist())
