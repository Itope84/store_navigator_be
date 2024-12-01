from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    with app.app_context():
        from .routes import init_routes

        init_routes(app)

    return app
