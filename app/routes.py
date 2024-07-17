from flask import jsonify, request, Flask

from .models import Product, Shelf, Store
from .svg_to_ndarray import FloorplanGrid, svg_to_ndarray


def init_routes(app: Flask):
    @app.route("/stores", methods=["GET"])
    def get_stores():
        stores = Store.query.all()
        return jsonify(stores)

    @app.route("/products", methods=["GET"])
    def get_products():
        # search
        search = request.args.get("search")
        if search:
            products = Product.query.filter(Product.name.ilike(f"%{search}%")).all()
        else:
            # no need to paginate for now. There's like 500+ results, the mobile app can handle the scrolling with a list builder
            products = Product.query.all()

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
