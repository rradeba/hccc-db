import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)

    app.config.from_object('config.Config')

    # CORS - Allow all origins for development and production
    CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from routes.health import bp as health_bp
    from routes.users import bp as users_bp
    from routes.leads import bp as leads_bp
    from routes.customers import bp as customers_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(leads_bp, url_prefix='/api/leads')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')

    return app


# Models import for migrations
from models.user import User, Lead, Customer  # noqa: E402


