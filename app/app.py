from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# from svg_to_ndarray import FloorplanGrid, svg_to_ndarray

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

print(database_url)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

