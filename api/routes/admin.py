from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
    create_access_token
)
from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId
from datetime import datetime, timedelta
import os
import json

admin_bp = Blueprint('admin', __name__)

# In production, store these securely (env or DB)
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@quickcart.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Simple credential check (hash in real app)
    if email != ADMIN_EMAIL or password != ADMIN_PASSWORD:
        return jsonify({'error': 'Invalid admin credentials'}), 401

    # Create token: identity must be string, extra claims carry role
    access_token = create_access_token(
        identity=email,
        additional_claims={'role': 'admin'},
        expires_delta=timedelta(hours=24)
    )

    return jsonify({
        'message': 'Admin login successful',
        'access_token': access_token,
        'admin': {'email': email, 'role': 'admin'}
    }), 200


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    # Check the 'role' claim
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    db = current_app.db

    # Statistics
    total_products   = db.products.count_documents({})
    total_orders     = db.orders.count_documents({})
    total_users      = db.users.count_documents({})
    pending_orders   = db.orders.count_documents({'status': 'pending'})
    completed_orders = db.orders.count_documents({'status': 'completed'})

    # Recent orders
    recent = list(
        db.orders
          .find()
          .sort('created_at', -1)
          .limit(5)
    )
    for o in recent:
        o['_id'] = str(o['_id'])
        o['user_id'] = str(o.get('user_id', ''))

    # Total revenue
    pipeline = [
        {'$match': {'status': 'completed'}},
        {'$group': {'_id': None, 'total': {'$sum': '$total_amount'}}}
    ]
    rev = list(db.orders.aggregate(pipeline))
    total_revenue = rev[0]['total'] if rev else 0

    return jsonify({
        'statistics': {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'total_revenue': total_revenue
        },
        'recent_orders': recent
    }), 200


@admin_bp.route('/products', methods=['GET', 'POST'])
@jwt_required()
def admin_products():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    db = current_app.db

    if request.method == 'GET':
        prods = list(db.products.find())
        for p in prods:
            p['_id'] = str(p['_id'])
        return jsonify({'products': prods}), 200

    # POST: create
    data = request.get_json() or {}
    required = ['name', 'price', 'category', 'subCategory', 'description']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    new_prod = {
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'image': data.get('image', []),
        'category': data['category'],
        'subCategory': data['subCategory'],
        'sizes': data.get('sizes', ['S','M','L']),
        'bestseller': bool(data.get('bestseller', False)),
        'created_at': datetime.utcnow()
    }
    res = db.products.insert_one(new_prod)
    new_prod['_id'] = str(res.inserted_id)

    return jsonify({'message': 'Product created', 'product': new_prod}), 201


@admin_bp.route('/products/<product_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_modify_product(product_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    db = current_app.db

    if request.method == 'PUT':
        data = request.get_json() or {}
        update = {}
        for f in ['name','description','price','image','category','subCategory','sizes','bestseller']:
            if f in data:
                update[f] = float(data[f]) if f == 'price' else data[f]
        update['updated_at'] = datetime.utcnow()

        res = db.products.update_one({'_id': ObjectId(product_id)}, {'$set': update})
        if res.matched_count == 0:
            return jsonify({'error': 'Product not found'}), 404

        prod = db.products.find_one({'_id': ObjectId(product_id)})
        prod['_id'] = str(prod['_id'])
        return jsonify({'message': 'Product updated', 'product': prod}), 200

    # DELETE
    res = db.products.delete_one({'_id': ObjectId(product_id)})
    if res.deleted_count == 0:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': 'Product deleted'}), 200


@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def admin_orders():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    db = current_app.db
    orders = list(db.orders.find().sort('created_at', -1))
    for o in orders:
        o['_id'] = str(o['_id'])
        o['user_id'] = str(o.get('user_id',''))
    return jsonify({'orders': orders}), 200


@admin_bp.route('/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def admin_update_order(order_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json() or {}
    status = data.get('status')
    if not status:
        return jsonify({'error': 'Status is required'}), 400

    valid = ['pending','processing','shipped','delivered','cancelled']
    if status not in valid:
        return jsonify({'error': 'Invalid status'}), 400

    db = current_app.db
    res = db.orders.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
    )
    if res.matched_count == 0:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify({'message': 'Order status updated'}), 200


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def admin_users():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    db = current_app.db
    users = list(db.users.find({}, {'password_hash': 0}))
    for u in users:
        u['_id'] = str(u['_id'])
    return jsonify({'users': users}), 200
