"""
User Resource: Handles registration, login, and info retrieval.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from models import db, User
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Namespace("users", description="User registration, login, and account management")

user_model = api.model("User", {
    "id": fields.Integer(readOnly=True, description="Unique user ID"),
    "username": fields.String(required=True, description="Username"),
})

register_model = api.model("Register", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

login_model = api.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

@api.route("/register")
class UserRegister(Resource):
    @api.expect(register_model)
    @api.response(201, "User registered")
    @api.response(400, "Username already exists")
    # PUBLIC_INTERFACE
    def post(self):
        """Register a new user."""
        data = api.payload
        if User.query.filter_by(username=data["username"]).first():
            return {"message": "Username already exists"}, 400
        hashed = generate_password_hash(data["password"]).decode("utf8")
        user = User(username=data["username"], password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered"}, 201

@api.route("/login")
class UserLogin(Resource):
    @api.expect(login_model)
    @api.response(200, "Login successful")
    @api.response(401, "Invalid credentials")
    # PUBLIC_INTERFACE
    def post(self):
        """Login and retrieve JWT token."""
        data = api.payload
        user = User.query.filter_by(username=data["username"]).first()
        if user and check_password_hash(user.password_hash, data["password"]):
            token = create_access_token(identity=user.id)
            return {"access_token": token, "user_id": user.id}, 200
        return {"message": "Invalid credentials"}, 401

@api.route("/me")
class UserMe(Resource):
    @api.marshal_with(user_model)
    @api.response(200, "Success")
    @jwt_required()
    # PUBLIC_INTERFACE
    def get(self):
        """Get currently logged in user's info."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user
