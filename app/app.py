from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# from svg_to_ndarray import FloorplanGrid, svg_to_ndarray

load_dotenv()

app = Flask(__name__)

# user = os.getenv("DATABASE_USER")
# password = os.getenv("DATABASE_PASSWORD")
# host = os.getenv("DATABASE_HOST")
# port = os.getenv("DATABASE_PORT")
# dbname = os.getenv("DATABASE_NAME")

database_url = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# get-route endpoint that takes start and end section_ids as query params and returns the route
# @app.route("/get-route", methods=["GET"])
# def get_route():
#     start = request.args.get("start")
#     end = request.args.get("end")

#     floorplan = FloorplanGrid("./floor_plan.svg")

#     route = floorplan.get_route(start, end)

#     return jsonify(route)


# @app.route("/get-grid", methods=["GET"])
# def get_grid():
#     grid = svg_to_ndarray("./floor_plan_mini.svg")

#     return jsonify(grid.tolist())


if __name__ == "__main__":
    # Listen on all public IPs on the network
    app.run(host="0.0.0.0", port=8000, debug=True)
