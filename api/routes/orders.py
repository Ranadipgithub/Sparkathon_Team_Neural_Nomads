from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def get_db():
    return current_app.db

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        print(f"Getting orders for user: {user_id}")
        
        orders = list(db.orders.find({'user_id': user_id}).sort('created_at', -1))
        print(f"Found {len(orders)} orders for user {user_id}")
        
        # Convert ObjectId to string
        for order in orders:
            order['_id'] = str(order['_id'])
            print(f"Order: {order['_id']}, Status: {order.get('status')}, Amount: {order.get('total_amount')}")
        
        return jsonify({
            'orders': orders,
            'total': len(orders)
        })
        
    except Exception as e:
        print(f"Get orders error: {e}")
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        
        order = db.orders.find_one({
            '_id': ObjectId(order_id),
            'user_id': user_id
        })
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order['_id'] = str(order['_id'])
        
        return jsonify(order)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        print(f"Create order request for user {user_id}: {data}")
        
        if not data:
            return jsonify({'error': 'Order data is required'}), 400
        
        # Get user's cart
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        cart_items = user.get('cart', [])
        print(f"Cart items for order: {len(cart_items)} items")
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total amount from cart items
        total_amount = 0
        order_items = []
        
        for cart_item in cart_items:
            product = db.products.find_one({'_id': cart_item['product_id']})
            if product:
                item_total = product['price'] * cart_item['quantity']
                total_amount += item_total
                
                order_items.append({
                    'product_id': str(cart_item['product_id']),
                    'product_name': product['name'],
                    'product_price': product['price'],
                    'size': cart_item['size'],
                    'quantity': cart_item['quantity'],
                    'item_total': item_total
                })
        
        # Add delivery fee
        delivery_fee = data.get('delivery_fee', 10)
        
        # Create order
        order_data = {
            'user_id': user_id,
            'items': order_items,
            'total_amount': total_amount,
            'delivery_fee': delivery_fee,
            'shipping_address': {
                'first_name': data.get('first_name', ''),
                'last_name': data.get('last_name', ''),
                'email': data.get('email', ''),
                'address': data.get('address', ''),
                'apartment': data.get('apartment', ''),
                'city': data.get('city', ''),
                'country': data.get('country', ''),
                'phone': data.get('phone', ''),
                'zip_code': data.get('zip_code', '')
            },
            'payment_method': data.get('payment_method', 'cod'),
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        print(f"Inserting order: {order_data}")
        
        result = db.orders.insert_one(order_data)
        order_id = str(result.inserted_id)
        
        print(f"Order created with ID: {order_id}")
        
        # Clear user's cart after successful order
        clear_result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': []}}
        )
        
        print(f"Cart cleared: {clear_result.modified_count} user updated")
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': {
                'order_id': order_id,
                'total_amount': total_amount + delivery_fee,
                'items_count': len(order_items)
            }
        }), 201
        
    except Exception as e:
        print(f"Create order error: {e}")
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        data = request.get_json()
        
        if not data or not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        status = data['status']
        
        result = db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'status': status,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'message': 'Order status updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
