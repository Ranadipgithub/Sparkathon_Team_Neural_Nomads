from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not getattr(user, 'is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'{field} is required'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
