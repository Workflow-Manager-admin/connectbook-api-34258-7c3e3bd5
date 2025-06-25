"""
Appointment Resource: CRUD for appointments.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from models import db, Appointment, Provider, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

api = Namespace("appointments", description="Appointment scheduling and booking")

appointment_model = api.model("Appointment", {
    "id": fields.Integer(readOnly=True),
    "user_id": fields.Integer(required=True),
    "provider_id": fields.Integer(required=True),
    "scheduled_time": fields.DateTime(required=True, dt_format='iso8601'),
    "status": fields.String,
    "created_at": fields.DateTime
})

create_appointment_model = api.model("CreateAppointment", {
    "provider_id": fields.Integer(required=True),
    "scheduled_time": fields.String(required=True, description="ISO 8601 datetime")
})

@api.route("")
class AppointmentList(Resource):
    @api.marshal_list_with(appointment_model)
    @api.response(200, "Success")
    @jwt_required()
    # PUBLIC_INTERFACE
    def get(self):
        """Get all appointments for the logged in user."""
        user_id = get_jwt_identity()
        return Appointment.query.filter_by(user_id=user_id).all()

    @api.expect(create_appointment_model)
    @api.marshal_with(appointment_model, code=201)
    @api.response(400, "Provider/time required")
    @jwt_required()
    # PUBLIC_INTERFACE
    def post(self):
        """Book a new appointment."""
        user_id = get_jwt_identity()
        data = api.payload
        try:
            scheduled = datetime.fromisoformat(data["scheduled_time"])
        except Exception as e:
            return {"message": "Invalid datetime format"}, 400
        appointment = Appointment(user_id=user_id, provider_id=data["provider_id"], scheduled_time=scheduled)
        db.session.add(appointment)
        db.session.commit()
        return appointment, 201

@api.route("/<int:id>")
@api.param('id', 'The appointment ID')
class AppointmentDetail(Resource):
    @api.marshal_with(appointment_model)
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @jwt_required()
    # PUBLIC_INTERFACE
    def get(self, id):
        """Get appointment by ID (must own appointment)."""
        user_id = get_jwt_identity()
        appt = Appointment.query.get(id)
        if not appt or appt.user_id != user_id:
            api.abort(404, "Appointment not found or access denied")
        return appt

    @api.expect(create_appointment_model)
    @api.marshal_with(appointment_model)
    @api.response(200, "Updated")
    @api.response(404, "Not found")
    @jwt_required()
    # PUBLIC_INTERFACE
    def put(self, id):
        """Reschedule or update appointment (user-only for their own appointments)."""
        user_id = get_jwt_identity()
        appt = Appointment.query.get(id)
        if not appt or appt.user_id != user_id:
            api.abort(404, "Appointment not found or access denied")
        data = api.payload
        if "scheduled_time" in data:
            try:
                appt.scheduled_time = datetime.fromisoformat(data["scheduled_time"])
            except Exception:
                return {"message": "Invalid datetime format"}, 400
        db.session.commit()
        return appt

    @api.response(204, "Deleted")
    @api.response(404, "Not found")
    @jwt_required()
    # PUBLIC_INTERFACE
    def delete(self, id):
        """Delete (cancel) appointment (user-only for their own appointments)."""
        user_id = get_jwt_identity()
        appt = Appointment.query.get(id)
        if not appt or appt.user_id != user_id:
            api.abort(404, "Appointment not found or access denied")
        db.session.delete(appt)
        db.session.commit()
        return '', 204
