from flask import Blueprint, request, jsonify, current_app
from models import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        # Get query parameters
        category = request.args.get('category')
        sub_category = request.args.get('subCategory')
        search = request.args.get('search')
        bestseller = request.args.get('bestseller')
        sort_by = request.args.get('sortBy', 'date')
        order = request.args.get('order', 'desc')
        limit = request.args.get('limit', type=int)
        
        # Build filters
        filters = {}
        
        if category:
            filters['category'] = category.split(',')
        
        if sub_category:
            filters['subCategory'] = sub_category.split(',')
        
        if search:
            filters['search'] = search
        
        if bestseller == 'true':
            filters['bestseller'] = True
        
        # Initialize Product model
        product_model = Product(current_app.db)
        
        # Get products
        products = product_model.find_all(filters, sort_by, order, limit)
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product_model = Product(current_app.db)
        product = product_model.find_by_id(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/bestsellers', methods=['GET'])
def get_bestsellers():
    try:
        limit = request.args.get('limit', 5, type=int)
        
        product_model = Product(current_app.db)
        products = product_model.find_bestsellers(limit)
        
        return jsonify({
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/latest', methods=['GET'])
def get_latest():
    try:
        limit = request.args.get('limit', 10, type=int)
        
        product_model = Product(current_app.db)
        products = product_model.find_latest(limit)
        
        return jsonify({
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/related/<product_id>', methods=['GET'])
def get_related_products(product_id):
    try:
        limit = request.args.get('limit', 5, type=int)
        
        product_model = Product(current_app.db)
        products = product_model.find_related(product_id, limit)
        
        return jsonify({
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
