from flask import jsonify, request, Flask

from .models import Product, Shelf
from .svg_to_ndarray import FloorplanGrid, svg_to_ndarray


def init_routes(app: Flask):
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
