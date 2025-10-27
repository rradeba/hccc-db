from flask import Blueprint, jsonify, request
from app import db
from models.user import Customer
from datetime import datetime

bp = Blueprint('customers', __name__)


@bp.get('/')
def list_customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers])

# Also respond without trailing slash
@bp.get('')
def list_customers_noslash():
    return list_customers()


@bp.post('/')
def create_customer():
    payload = request.get_json(silent=True) or {}

    customer = Customer(
        name=(payload.get('name') or '').strip(),
        email=(payload.get('email') or '').strip().lower() or None,
        phone=(payload.get('phone') or '').strip() or None,
        address=(payload.get('address') or '').strip() or None,
        source=(payload.get('source') or '').strip() or None,
        join_date=datetime.fromisoformat(payload['joinDate']).date() if payload.get('joinDate') else None,
        total_spent=float(payload.get('totalSpent') or 0),
        service_count=int(payload.get('serviceCount') or 0),
        last_service=datetime.fromisoformat(payload['lastService']).date() if payload.get('lastService') else None,
        rating=int(payload.get('rating') or 5),
        services=payload.get('services') or [],
        review_status=(payload.get('reviewStatus') or 'none').strip()
    )

    if not customer.name:
        return jsonify({'error': 'Name is required'}), 400

    try:
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to create customer'}), 500

# Also accept POST without trailing slash
@bp.post('')
def create_customer_noslash():
    return create_customer()


@bp.patch('/<int:customer_id>')
def update_customer(customer_id: int):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    payload = request.get_json(silent=True) or {}

    review_status = payload.get('reviewStatus')
    rating = payload.get('rating')
    add_service = payload.get('addService')  # { type, date, amount }

    if review_status is not None:
        customer.review_status = (review_status or 'none').strip()
    if rating is not None:
        try:
            customer.rating = int(rating)
        except Exception:
            pass
    if add_service:
        try:
            service_type = (add_service.get('type') or add_service.get('name') or '').strip()
            service_date_str = add_service.get('date')
            service_amount = float(add_service.get('amount') or 0)
            # Append to JSON services list
            if not isinstance(customer.services, list) or customer.services is None:
                customer.services = []
            entry = {
                'type': service_type,
                'date': service_date_str,
                'amount': service_amount,
                'status': add_service.get('status') or 'Completed'
            }
            # Reassign the JSON list so SQLAlchemy detects changes
            existing_services = customer.services or []
            if not isinstance(existing_services, list):
                existing_services = []
            customer.services = existing_services + [entry]
            # Update aggregates
            customer.total_spent = float(customer.total_spent or 0) + service_amount
            customer.service_count = int(customer.service_count or 0) + 1
            # Update last_service if date provided
            if service_date_str:
                try:
                    customer.last_service = datetime.fromisoformat(service_date_str).date()
                except Exception:
                    pass
        except Exception:
            pass

    try:
        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to update customer'}), 500


@bp.delete('/<int:customer_id>')
def delete_customer(customer_id: int):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete customer'}), 500


