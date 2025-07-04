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

# Initialize extensions
jwt = JWTManager(app)
CORS(app)

# MongoDB connection
try:
    client = MongoClient(app.config['MONGODB_URI'])
    db = client.get_default_database()
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Make db available globally
app.db = db

# Import routes
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        db.command('ping')
        return jsonify({'status': 'healthy', 'message': 'API is running', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'message': 'Database connection failed', 'error': str(e)}), 500

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
    app.run(debug=True, port=5328)
