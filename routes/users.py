from flask import Blueprint, jsonify, request
from app import db
from models.user import User

bp = Blueprint('users', __name__)


@bp.get('/')
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([u.to_dict() for u in users])


@bp.post('/')
def create_user():
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    email = (payload.get('email') or '').strip().lower()

    errors = {}
    if not name:
        errors['name'] = 'Name is required.'
    if not email:
        errors['email'] = 'Email is required.'
    if errors:
        return jsonify({'errors': errors}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'errors': {'email': 'Email already exists.'}}), 409

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201




