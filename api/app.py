from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ecommerce')

# Initialize CORS with proper configuration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True
    }
})

# Initialize JWT
jwt = JWTManager(app)

jwt = JWTManager(app)

# Return 401 (not 422) when no token is present
@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"error": "Authorization token required"}), 401

# Return 401 when token is invalid (e.g. bad signature)
@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({"error": "Invalid token"}), 401

# Return 401 when token has expired
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401


# MongoDB connection
try:
    client = MongoClient(app.config['MONGODB_URI'])
    db = client.get_default_database()
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

# Make db available globally
app.db = db

# Import routes after app initialization
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from routes.admin import admin_bp
from VoiceAssistance import voiceBlueprint

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(voiceBlueprint, url_prefix='/voiceAssistance')

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        if db is None:
            return jsonify({'status': 'unhealthy', 'message': 'Database not connected'}), 500
        # Test MongoDB connection
        db.command('ping')
        return jsonify({'status': 'healthy', 'message': 'API is running', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'message': 'Database connection failed', 'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'E-commerce API is running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth/*',
            'products': '/api/products/*',
            'cart': '/api/cart/*',
            'orders': '/api/orders/*',
            'admin': '/api/admin/*'
        }
    })

@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'message': 'E-commerce API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'health': '/api/health',
            'auth': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login',
                'profile': 'GET /api/auth/profile',
                'logout': 'POST /api/auth/logout'
            },
            'products': {
                'list': 'GET /api/products/',
                'get': 'GET /api/products/{id}',
                'bestsellers': 'GET /api/products/bestsellers',
                'latest': 'GET /api/products/latest',
                'related': 'GET /api/products/related/{id}'
            },
            'cart': {
                'get': 'GET /api/cart/',
                'add': 'POST /api/cart/add',
                'update': 'PUT /api/cart/update',
                'remove': 'DELETE /api/cart/remove',
                'clear': 'DELETE /api/cart/clear'
            },
            'orders': {
                'list': 'GET /api/orders/',
                'get': 'GET /api/orders/{id}',
                'create': 'POST /api/orders/create',
                'update_status': 'PUT /api/orders/{id}/status'
            },
            'admin': {
                'login': 'POST /api/admin/login',
                'dashboard': 'GET /api/admin/dashboard',
                'products': 'GET/POST/PUT/DELETE /api/admin/products',
                'orders': 'GET /api/admin/orders',
                'users': 'GET /api/admin/users'
            }
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Custom JSON encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app.json_encoder = JSONEncoder

if __name__ == '__main__':
    app.run(debug=True, port=5328, host='0.0.0.0')
