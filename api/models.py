from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class BaseModel:
    def __init__(self, db):
        self.db = db
    
    def to_dict(self, doc):
        """Convert MongoDB document to dictionary with string ObjectId"""
        if doc is None:
            return None
        doc['_id'] = str(doc['_id'])
        return doc

class User(BaseModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = db.users
    
    def create(self, name, email, password):
        """Create a new user"""
        user_data = {
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(user_data)
        return self.find_by_id(result.inserted_id)
    
    def find_by_email(self, email):
        """Find user by email"""
        user = self.collection.find_one({'email': email})
        return self.to_dict(user)
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        user = self.collection.find_one({'_id': user_id})
        return self.to_dict(user)
    
    def verify_password(self, user, password):
        """Verify user password"""
        return check_password_hash(user['password_hash'], password)

class Product(BaseModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = db.products
    
    def create(self, product_data):
        """Create a new product"""
        product_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(product_data)
        return self.find_by_id(result.inserted_id)
    
    def find_all(self, filters=None, sort_by='date', order='desc', limit=None):
        """Find all products with optional filters"""
        query = {}
        
        if filters:
            if 'category' in filters:
                query['category'] = {'$in': filters['category']}
            if 'subCategory' in filters:
                query['subCategory'] = {'$in': filters['subCategory']}
            if 'search' in filters:
                query['name'] = {'$regex': filters['search'], '$options': 'i'}
            if 'bestseller' in filters:
                query['bestseller'] = filters['bestseller']
        
        # Sort configuration
        sort_direction = -1 if order == 'desc' else 1
        sort_field = 'price' if sort_by == 'price' else 'date'
        
        cursor = self.collection.find(query).sort(sort_field, sort_direction)
        
        if limit:
            cursor = cursor.limit(limit)
        
        products = []
        for product in cursor:
            products.append(self.to_dict(product))
        
        return products
    
    def find_by_id(self, product_id):
        """Find product by ID"""
        if isinstance(product_id, ObjectId):
            query = {'_id': product_id}
        else:
            # Try both string ID and ObjectId
            query = {'$or': [{'_id': product_id}, {'_id': ObjectId(product_id) if ObjectId.is_valid(product_id) else None}]}
        
        product = self.collection.find_one(query)
        return self.to_dict(product)
    
    def find_bestsellers(self, limit=5):
        """Find bestseller products"""
        products = []
        cursor = self.collection.find({'bestseller': True}).limit(limit)
        for product in cursor:
            products.append(self.to_dict(product))
        return products
    
    def find_latest(self, limit=10):
        """Find latest products"""
        products = []
        cursor = self.collection.find().sort('date', -1).limit(limit)
        for product in cursor:
            products.append(self.to_dict(product))
        return products
    
    def find_related(self, product_id, limit=5):
        """Find related products"""
        product = self.find_by_id(product_id)
        if not product:
            return []
        
        query = {
            'category': product['category'],
            'subCategory': product['subCategory'],
            '_id': {'$ne': product_id if not isinstance(product_id, ObjectId) else product_id}
        }
        
        products = []
        cursor = self.collection.find(query).limit(limit)
        for p in cursor:
            products.append(self.to_dict(p))
        return products

class Cart(BaseModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = db.cart_items
    
    def add_item(self, user_id, product_id, size, quantity=1):
        """Add item to cart"""
        # Check if item already exists
        existing_item = self.collection.find_one({
            'user_id': user_id,
            'product_id': product_id,
            'size': size
        })
        
        if existing_item:
            # Update quantity
            self.collection.update_one(
                {'_id': existing_item['_id']},
                {'$inc': {'quantity': quantity}}
            )
            return self.to_dict(self.collection.find_one({'_id': existing_item['_id']}))
        else:
            # Create new item
            cart_item = {
                'user_id': user_id,
                'product_id': product_id,
                'size': size,
                'quantity': quantity,
                'created_at': datetime.utcnow()
            }
            result = self.collection.insert_one(cart_item)
            return self.to_dict(self.collection.find_one({'_id': result.inserted_id}))
    
    def get_user_cart(self, user_id):
        """Get all cart items for a user"""
        items = []
        cursor = self.collection.find({'user_id': user_id})
        for item in cursor:
            items.append(self.to_dict(item))
        return items
    
    def update_quantity(self, user_id, product_id, size, quantity):
        """Update item quantity"""
        if quantity <= 0:
            return self.remove_item(user_id, product_id, size)
        
        result = self.collection.update_one(
            {'user_id': user_id, 'product_id': product_id, 'size': size},
            {'$set': {'quantity': quantity}}
        )
        return result.modified_count > 0
    
    def remove_item(self, user_id, product_id, size):
        """Remove item from cart"""
        result = self.collection.delete_one({
            'user_id': user_id,
            'product_id': product_id,
            'size': size
        })
        return result.deleted_count > 0
    
    def clear_cart(self, user_id):
        """Clear all items from user's cart"""
        result = self.collection.delete_many({'user_id': user_id})
        return result.deleted_count

class Order(BaseModel):
    def __init__(self, db):
        super().__init__(db)
        self.collection = db.orders
    
    def create(self, order_data):
        """Create a new order"""
        order_data['created_at'] = datetime.utcnow()
        order_data['status'] = 'pending'
        result = self.collection.insert_one(order_data)
        return self.find_by_id(result.inserted_id)
    
    def find_by_user(self, user_id):
        """Find all orders for a user"""
        orders = []
        cursor = self.collection.find({'user_id': user_id}).sort('created_at', -1)
        for order in cursor:
            orders.append(self.to_dict(order))
        return orders
    
    def find_by_id(self, order_id):
        """Find order by ID"""
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        order = self.collection.find_one({'_id': order_id})
        return self.to_dict(order)
    
    def update_status(self, order_id, status):
        """Update order status"""
        if isinstance(order_id, str):
            order_id = ObjectId(order_id)
        result = self.collection.update_one(
            {'_id': order_id},
            {'$set': {'status': status}}
        )
        return result.modified_count > 0
