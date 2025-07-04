from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Initialize User model
        user_model = User(current_app.db)
        
        # Check if user already exists
        if user_model.find_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = user_model.create(data['name'], data['email'], data['password'])
        
        # Create access token
        access_token = create_access_token(identity=user['_id'])
        
        # Remove password hash from response
        user.pop('password_hash', None)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Initialize User model
        user_model = User(current_app.db)
        
        # Find user
        user = user_model.find_by_email(data['email'])
        
        if not user or not user_model.verify_password(user, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user['_id'])
        
        # Remove password hash from response
        user.pop('password_hash', None)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user_model = User(current_app.db)
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove password hash from response
        user.pop('password_hash', None)
        
        return jsonify({'user': user}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a real application, you might want to blacklist the token
    return jsonify({'message': 'Logout successful'}), 200
