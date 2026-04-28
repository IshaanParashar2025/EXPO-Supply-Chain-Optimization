"""Flask extensions initialized with the init_app pattern."""
from flask_cors import CORS
from pymongo import MongoClient


class MongoDB:
    """PyMongo wrapper following the Flask extension pattern."""

    def __init__(self, app=None):
        self.client = None
        self.db = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        uri = app.config.get('MONGO_URI')
        self.client = MongoClient(uri)
        self.db = self.client.get_default_database()

        @app.teardown_appcontext
        def close_connection(exception):
            if self.client is not None:
                self.client.close()


cors = CORS(resources={r"/*": {"origins": "*"}})
mongo = MongoDB()

