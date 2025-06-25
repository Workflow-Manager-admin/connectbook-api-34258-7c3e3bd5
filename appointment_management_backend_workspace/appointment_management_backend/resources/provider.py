"""
Provider Resource: CRUD for service providers.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from models import db, Provider, User
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("providers", description="Provider CRUD and management")

provider_model = api.model("Provider", {
    "id": fields.Integer(readOnly=True),
    "name": fields.String(required=True),
    "specialty": fields.String(),
    "user_id": fields.Integer(),
})

@api.route("")
class ProviderList(Resource):
    @api.marshal_list_with(provider_model)
    @api.response(200, "Success")
    # PUBLIC_INTERFACE
    def get(self):
        """List all providers."""
        return Provider.query.all()

    @api.expect(provider_model)
    @api.response(201, "Provider created")
    @jwt_required()
    # PUBLIC_INTERFACE
    def post(self):
        """Create a new provider (must be authenticated user)."""
        data = api.payload
        user_id = get_jwt_identity()
        provider = Provider(name=data["name"], specialty=data.get("specialty", ""), user_id=user_id)
        db.session.add(provider)
        db.session.commit()
        return provider, 201

@api.route("/<int:id>")
@api.param('id', 'Provider ID')
class ProviderDetail(Resource):
    @api.marshal_with(provider_model)
    @api.response(200, "Success")
    @api.response(404, "Not found")
    # PUBLIC_INTERFACE
    def get(self, id):
        """Get provider by ID."""
        provider = Provider.query.get(id)
        if not provider:
            api.abort(404, "Provider not found")
        return provider

    @api.expect(provider_model)
    @api.response(200, "Updated")
    @api.response(404, "Not found")
    @jwt_required()
    # PUBLIC_INTERFACE
    def put(self, id):
        """Update provider info."""
        provider = Provider.query.get(id)
        if not provider:
            api.abort(404, "Provider not found")
        data = api.payload
        provider.name = data.get("name", provider.name)
        provider.specialty = data.get("specialty", provider.specialty)
        db.session.commit()
        return provider

    @api.response(204, "Deleted")
    @api.response(404, "Not found")
    @jwt_required()
    # PUBLIC_INTERFACE
    def delete(self, id):
        """Delete provider by id."""
        provider = Provider.query.get(id)
        if not provider:
            api.abort(404, "Provider not found")
        db.session.delete(provider)
        db.session.commit()
        return '', 204
