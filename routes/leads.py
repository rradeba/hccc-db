from flask import Blueprint, jsonify, request
from app import db
from models.user import Lead
import json

bp = Blueprint('leads', __name__)


@bp.get('/')
def list_leads():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return jsonify([lead.to_dict() for lead in leads])

# Also respond without trailing slash
@bp.get('')
def list_leads_noslash():
    return list_leads()


@bp.post('/')
def create_lead():
    payload = request.get_json(silent=True) or {}
    
    # Extract and validate required fields
    first_name = (payload.get('firstName') or '').strip()
    last_name = (payload.get('lastName') or '').strip()
    email = (payload.get('email') or '').strip().lower()
    phone = (payload.get('phone') or '').strip()
    street_address = (payload.get('streetAddress') or '').strip()
    city = (payload.get('city') or '').strip()
    state = (payload.get('state') or '').strip()
    zip_code = (payload.get('zip') or '').strip()
    referrer = (payload.get('referrer') or '').strip()
    service = payload.get('service', [])
    other_details = (payload.get('otherDetails') or '').strip()
    notes = (payload.get('notes') or '').strip()
    
    # Build combined fields
    name = f"{first_name} {last_name}".strip()
    address = f"{street_address}, {city}, {state} {zip_code}".strip()
    
    # Convert service array to JSON string
    if isinstance(service, list):
        service_json = json.dumps(service)
    else:
        service_json = json.dumps([service] if service else [])
    
    # Validate required fields
    errors = {}
    if not first_name:
        errors['firstName'] = 'First name is required'
    if not last_name:
        errors['lastName'] = 'Last name is required'
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email:
        errors['email'] = 'Valid email is required'
    if not phone:
        errors['phone'] = 'Phone is required'
    if not street_address:
        errors['streetAddress'] = 'Street address is required'
    if not city:
        errors['city'] = 'City is required'
    if not state:
        errors['state'] = 'State is required'
    if not zip_code:
        errors['zip'] = 'ZIP code is required'
    if not referrer:
        errors['referrer'] = 'Referrer is required'
    if not service or (isinstance(service, list) and len(service) == 0):
        errors['service'] = 'At least one service must be selected'
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Create lead
    lead = Lead(
        first_name=first_name,
        last_name=last_name,
        name=name,
        email=email,
        phone=phone,
        street_address=street_address,
        city=city,
        state=state,
        zip_code=zip_code,
        address=address,
        referrer=referrer,
        service=service_json,
        other_details=other_details,
        notes=notes
    )
    
    try:
        db.session.add(lead)
        db.session.commit()
        return jsonify(lead.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create lead'}), 500

# Also accept POST without trailing slash
@bp.post('')
def create_lead_noslash():
    return create_lead()


@bp.delete('/<int:lead_id>')
def delete_lead(lead_id: int):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    try:
        db.session.delete(lead)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete lead'}), 500
