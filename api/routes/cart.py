from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

def get_db():
    return current_app.db

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        print(f"Getting cart for user: {user_id}")
        
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cart_items = user.get('cart', [])
        print(f"Raw cart items from DB: {cart_items}")
        
        # Populate cart items with product details
        populated_cart = []
        for item in cart_items:
            product_id = item['product_id']
            product = db.products.find_one({'_id': product_id})
            
            if product:
                product['_id'] = str(product['_id'])
                populated_cart.append({
                    'product_id': str(item['product_id']),
                    'product': product,
                    'size': item['size'],
                    'quantity': item['quantity'],
                    'added_at': item.get('added_at')
                })
        
        print(f"Populated cart: {len(populated_cart)} items")
        
        return jsonify({
            'success': True,
            'cart_items': populated_cart,
            'total_items': len(populated_cart)
        })
        
    except Exception as e:
        print(f"Cart get error: {e}")
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        print(f"Add to cart request: {data} for user: {user_id}")
        
        if not data or not data.get('product_id'):
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        size = data.get('size', 'M')
        quantity = int(data.get('quantity', 1))
        
        # Verify product exists
        product = db.products.find_one({'_id': product_id})
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get user's current cart
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cart = user.get('cart', [])
        print(f"Current cart before adding: {cart}")
        
        # Check if item already exists in cart
        item_found = False
        for i, item in enumerate(cart):
            if str(item['product_id']) == str(product_id) and item['size'] == size:
                cart[i]['quantity'] += quantity
                item_found = True
                print(f"Updated existing item quantity to: {cart[i]['quantity']}")
                break
        
        # If item not found, add new item
        if not item_found:
            cart_item = {
                'product_id': product_id,
                'size': size,
                'quantity': quantity,
                'added_at': datetime.utcnow()
            }
            cart.append(cart_item)
            print(f"Added new item to cart: {cart_item}")
        
        # Update user's cart in database
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': cart}}
        )
        
        print(f"Cart update result: modified_count={result.modified_count}")
        print(f"Final cart: {cart}")
        
        # Verify the update
        updated_user = db.users.find_one({'_id': ObjectId(user_id)})
        print(f"Verified cart in DB: {updated_user.get('cart', [])}")
        
        return jsonify({
            'success': True,
            'message': 'Product added to cart successfully',
            'cart_count': len(cart)
        })
        
    except Exception as e:
        print(f"Add to cart error: {e}")
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_cart():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('product_id'):
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        size = data.get('size', 'M')
        quantity = int(data.get('quantity', 1))
        
        # Get user's current cart
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cart = user.get('cart', [])
        
        # Find and update the item
        item_found = False
        for i, item in enumerate(cart):
            if str(item['product_id']) == str(product_id) and item['size'] == size:
                if quantity <= 0:
                    cart.pop(i)
                else:
                    cart[i]['quantity'] = quantity
                item_found = True
                break
        
        if not item_found:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Update user's cart in database
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': cart}}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Failed to update cart'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Cart updated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('product_id'):
            return jsonify({'error': 'Product ID is required'}), 400
        
        product_id = data['product_id']
        size = data.get('size', 'M')
        
        # Get user's current cart
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cart = user.get('cart', [])
        
        # Find and remove the item
        item_found = False
        for i, item in enumerate(cart):
            if str(item['product_id']) == str(product_id) and item['size'] == size:
                cart.pop(i)
                item_found = True
                break
        
        if not item_found:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Update user's cart in database
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': cart}}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Failed to update cart'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Product removed from cart successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        
        # Clear cart
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': []}}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Failed to clear cart'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
