from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() + 'Z',
        }


class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(240), nullable=False)  # Combined name
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(500), nullable=False)  # Combined address
    referrer = db.Column(db.String(100), nullable=False)
    service = db.Column(db.Text, nullable=False)  # JSON array of services
    other_details = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'address': self.address,
            'referrer': self.referrer,
            'service': self.service,
            'other_details': self.other_details,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() + 'Z',
        }


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(64))
    address = db.Column(db.String(512))
    source = db.Column(db.String(128))
    join_date = db.Column(db.Date)
    total_spent = db.Column(db.Float, default=0)
    service_count = db.Column(db.Integer, default=0)
    last_service = db.Column(db.Date)
    rating = db.Column(db.Integer, default=5)
    services = db.Column(db.JSON)
    review_status = db.Column(db.String(20), default='none')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'source': self.source,
            'join_date': self.join_date.isoformat() + 'Z' if self.join_date else None,
            'total_spent': self.total_spent,
            'service_count': self.service_count,
            'last_service': self.last_service.isoformat() + 'Z' if self.last_service else None,
            'rating': self.rating,
            'services': self.services or [],
            'review_status': self.review_status or 'none',
            'created_at': self.created_at.isoformat() + 'Z',
        }

