import time
from flask import Flask, jsonify, request

from svg_to_ndarray import FloorplanGrid, svg_to_ndarray

app = Flask(__name__)


# get-route endpoint that takes start and end section_ids as query params and returns the route
@app.route("/get-route", methods=["GET"])
def get_route():
    start = request.args.get("start")
    end = request.args.get("end")

    floorplan = FloorplanGrid("./floor_plan.svg")

    route = floorplan.get_route(start, end)

    return jsonify(route)


@app.route("/get-grid", methods=["GET"])
def get_grid():
    grid = svg_to_ndarray("./floor_plan_mini.svg")

    return jsonify(grid.tolist())


if __name__ == "__main__":
    # Listen on all public IPs on the network
    app.run(host="0.0.0.0", port=8000, debug=True)
