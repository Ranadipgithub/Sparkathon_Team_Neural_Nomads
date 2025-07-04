from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from bson.errors import InvalidId
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
        
    try:
        db = current_app.db
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
            
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
        # Check if user already exists
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'User already exists with this email'}), 400
            
        # Create new user
        hashed_password = generate_password_hash(password)
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'created_at': ObjectId().generation_time
        }
        
        result = db.users.insert_one(user_data)
        
        # Create access token
        access_token = create_access_token(identity=str(result.inserted_id))
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': str(result.inserted_id),
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
        
    try:
        db = current_app.db
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
            
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
            
        # Find user
        user = db.users.find_one({'email': email})
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
            
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
            
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_profile():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
        
    try:
        db = current_app.db
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
            
        user_id = get_jwt_identity()
        
        try:
            obj_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({'error': 'Invalid user ID'}), 400
            
        user = db.users.find_one({'_id': obj_id})
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'success': True,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
        
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })
