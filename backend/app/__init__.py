"""Application factory for the Supply Chain Flask backend."""
from flask import Flask

from app.config import Config
from app.extensions import cors, mongo
from app.routes import suppliers, manufacturers, distributors, inventory, orders, logistics, dashboard


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False  # Match Express behavior

    # Initialize extensions
    cors.init_app(app)
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(suppliers.bp, url_prefix='/api/suppliers')
    app.register_blueprint(manufacturers.bp, url_prefix='/api/manufacturers')
    app.register_blueprint(distributors.bp, url_prefix='/api/distributors')
    app.register_blueprint(inventory.bp, url_prefix='/api/inventory')
    app.register_blueprint(orders.bp, url_prefix='/api/orders')
    app.register_blueprint(logistics.bp, url_prefix='/api/logistics')
    app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')

    @app.route('/')
    def health_check():
        return {'message': '\U0001f69a Supply Chain MVC API Running on port 5000'}

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Global error handler."""
        import traceback
        traceback.print_exc()
        response = {'success': False, 'error': str(error)}
        status_code = getattr(error, 'code', 500)
        return response, status_code

    return app

