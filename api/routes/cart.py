from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Cart, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        cart_model = Cart(current_app.db)
        product_model = Product(current_app.db)
        
        cart_items = cart_model.get_user_cart(user_id)
        
        # Populate product details
        for item in cart_items:
            product = product_model.find_by_id(item['product_id'])
            item['product'] = product
        
        return jsonify({
            'cart_items': cart_items
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('product_id') or not data.get('size'):
            return jsonify({'error': 'Product ID and size are required'}), 400
        
        # Check if product exists
        product_model = Product(current_app.db)
        product = product_model.find_by_id(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Add to cart
        cart_model = Cart(current_app.db)
        cart_item = cart_model.add_item(
            user_id,
            data['product_id'],
            data['size'],
            data.get('quantity', 1)
        )
        
        return jsonify({
            'message': 'Item added to cart successfully',
            'cart_item': cart_item
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/update', methods=['PUT', 'PATCH'])
@jwt_required()
def update_cart():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('product_id') or not data.get('size') or 'quantity' not in data:
            return jsonify({'error': 'Product ID, size, and quantity are required'}), 400
        
        cart_model = Cart(current_app.db)
        success = cart_model.update_quantity(
            user_id,
            data['product_id'],
            data['size'],
            data['quantity']
        )
        
        if not success:
            return jsonify({'error': 'Cart item not found'}), 404
        
        return jsonify({'message': 'Cart updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('product_id') or not data.get('size'):
            return jsonify({'error': 'Product ID and size are required'}), 400
        
        cart_model = Cart(current_app.db)
        success = cart_model.remove_item(
            user_id,
            data['product_id'],
            data['size']
        )
        
        if not success:
            return jsonify({'error': 'Cart item not found'}), 404
        
        return jsonify({'message': 'Item removed from cart successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    try:
        user_id = get_jwt_identity()
        cart_model = Cart(current_app.db)
        
        deleted_count = cart_model.clear_cart(user_id)
        
        return jsonify({
            'message': 'Cart cleared successfully',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
