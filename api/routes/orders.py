from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, Cart, Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()
        order_model = Order(current_app.db)
        orders = order_model.find_by_user(user_id)
        
        return jsonify({
            'orders': orders
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        order_model = Order(current_app.db)
        order = order_model.find_by_id(order_id)
        
        if not order or order['user_id'] != user_id:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({'order': order}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'address', 'city', 'country', 'phone', 'zip_code', 'payment_method']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Get cart items
        cart_model = Cart(current_app.db)
        product_model = Product(current_app.db)
        cart_items = cart_model.get_user_cart(user_id)
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total amount and prepare order items
        total_amount = 0
        order_items = []
        
        for cart_item in cart_items:
            product = product_model.find_by_id(cart_item['product_id'])
            if product:
                item_total = product['price'] * cart_item['quantity']
                total_amount += item_total
                
                order_items.append({
                    'product_id': cart_item['product_id'],
                    'size': cart_item['size'],
                    'quantity': cart_item['quantity'],
                    'price': product['price'],
                    'product_name': product['name']
                })
        
        # Create order
        order_data = {
            'user_id': user_id,
            'total_amount': total_amount,
            'delivery_fee': data.get('delivery_fee', 10.0),
            'payment_method': data['payment_method'],
            'delivery_info': {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'address': data['address'],
                'apartment': data.get('apartment', ''),
                'city': data['city'],
                'country': data['country'],
                'phone': data['phone'],
                'zip_code': data['zip_code']
            },
            'items': order_items
        }
        
        order_model = Order(current_app.db)
        order = order_model.create(order_data)
        
        # Clear cart after successful order
        cart_model.clear_cart(user_id)
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        order_model = Order(current_app.db)
        order = order_model.find_by_id(order_id)
        
        if not order or order['user_id'] != user_id:
            return jsonify({'error': 'Order not found'}), 404
        
        success = order_model.update_status(order_id, data['status'])
        
        if not success:
            return jsonify({'error': 'Failed to update order status'}), 500
        
        updated_order = order_model.find_by_id(order_id)
        
        return jsonify({
            'message': 'Order status updated successfully',
            'order': updated_order
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
