"""
Flask Application Entry Point for Appointment Management Backend

- User registration and token-based authentication (Mock JWT)
- CRUD for appointments
- CRUD for providers
- RESTful endpoints (documented with Swagger)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# PUBLIC_INTERFACE
def create_app():
    """Create Flask app instance and initialize extensions."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Replace with env in real deployment
    app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"  # Replace with env in real deployment

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Setup API and Namespace
    api = Api(
        app,
        version="1.0",
        title="Appointment Management API",
        description="API for registering users, managing appointments, and connecting with providers.",
        doc="/docs"
    )

    # Import namespaces here to avoid circular imports
    from resources.user import api as user_ns
    from resources.provider import api as provider_ns
    from resources.appointment import api as appointment_ns

    # Register Namespaces
    api.add_namespace(user_ns, path="/users")
    api.add_namespace(provider_ns, path="/providers")
    api.add_namespace(appointment_ns, path="/appointments")

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

app = create_app()
