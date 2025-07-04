from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime

products_bp = Blueprint('products', __name__)

def get_db():
    return current_app.db

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get query parameters
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        search = request.args.get('search')
        sort_by = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')
        limit = request.args.get('limit', type=int)
        
        # Build query
        query = {}
        if category:
            query['category'] = category
        if subcategory:
            query['subCategory'] = subcategory
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}
        
        # Sort configuration
        sort_direction = -1 if order == 'desc' else 1
        sort_field = 'price' if sort_by == 'price' else 'date'
        
        cursor = db.products.find(query).sort(sort_field, sort_direction)
        
        if limit:
            cursor = cursor.limit(limit)
        
        products = []
        for product in cursor:
            product['_id'] = str(product['_id'])
            products.append(product)
        
        return jsonify({
            'success': True,
            'products': products,
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Try to find product by string ID first
        product = db.products.find_one({'_id': product_id})
        
        # If not found and it's a valid ObjectId, try ObjectId
        if not product and ObjectId.is_valid(product_id):
            try:
                product = db.products.find_one({'_id': ObjectId(product_id)})
            except:
                pass
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        product['_id'] = str(product['_id'])
        
        return jsonify({
            'success': True,
            'product': product
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/bestsellers', methods=['GET'])
def get_bestsellers():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        limit = request.args.get('limit', 5, type=int)
        
        products = []
        cursor = db.products.find({'bestseller': True}).limit(limit)
        for product in cursor:
            product['_id'] = str(product['_id'])
            products.append(product)
        
        return jsonify({
            'success': True,
            'products': products
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/latest', methods=['GET'])
def get_latest():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        limit = request.args.get('limit', 10, type=int)
        
        products = []
        cursor = db.products.find().sort('date', -1).limit(limit)
        for product in cursor:
            product['_id'] = str(product['_id'])
            products.append(product)
        
        return jsonify({
            'success': True,
            'products': products
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/<product_id>/related', methods=['GET'])
def get_related_products(product_id):
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Get the main product first
        product = db.products.find_one({'_id': product_id})
        if not product and ObjectId.is_valid(product_id):
            try:
                product = db.products.find_one({'_id': ObjectId(product_id)})
            except:
                pass
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        limit = request.args.get('limit', 5, type=int)
        
        # Find related products in same category/subcategory
        query = {
            'category': product['category'],
            'subCategory': product['subCategory'],
            '_id': {'$ne': product['_id']}
        }
        
        products = []
        cursor = db.products.find(query).limit(limit)
        for p in cursor:
            p['_id'] = str(p['_id'])
            products.append(p)
        
        return jsonify({
            'success': True,
            'products': products
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
