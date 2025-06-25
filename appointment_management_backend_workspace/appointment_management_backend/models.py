"""
Database models for User, Provider, and Appointment.
"""

from app import db
from datetime import datetime

# PUBLIC_INTERFACE
class User(db.Model):
    """User model for user registration and authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_provider = db.Column(db.Boolean, default=False)

    # For convenience: users can also be providers (e.g., a doctor using the platform)
    provider = db.relationship('Provider', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

# PUBLIC_INTERFACE
class Provider(db.Model):
    """Provider model (doctors, tutors, etc.)."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointments = db.relationship('Appointment', backref='provider', lazy=True)

    def __repr__(self):
        return f'<Provider {self.name}>'

# PUBLIC_INTERFACE
class Appointment(db.Model):
    """Appointment model representing bookings."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="scheduled")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='appointments')

    def __repr__(self):
        return f'<Appointment {self.id} @ {self.scheduled_time}>'
