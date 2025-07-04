import sys
import os
import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
from werkzeug.security import generate_password_hash

# Add the parent directory to the path so we can import from api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def seed_database():
    try:
        # MongoDB connection
        MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ecommerce')
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        
        print("🌱 Starting database seeding...")
        
        # Clear existing data
        db.products.delete_many({})
        db.users.delete_many({})
        db.carts.delete_many({})
        db.orders.delete_many({})
        print("🧹 Collections cleared!")
        
        # Sample products data with working image URLs
        products_data = [
            {
                "_id": "aaaaa",
                "name": "Women Round Neck Cotton Top",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 100,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Women",
                "subCategory": "Topwear",
                "sizes": ["S", "M", "L"],
                "date": datetime.utcnow(),
                "bestseller": True
            },
            {
                "_id": "aaaab",
                "name": "Men Round Neck Pure Cotton T-shirt",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 200,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Men",
                "subCategory": "Topwear",
                "sizes": ["S", "M", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaac",
                "name": "Girls Round Neck Cotton Top",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 220,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Kids",
                "subCategory": "Topwear",
                "sizes": ["S", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": True
            },
            {
                "_id": "aaaad",
                "name": "Men Round Neck Pure Cotton T-shirt",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 110,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Men",
                "subCategory": "Topwear",
                "sizes": ["S", "M", "XXL"],
                "date": datetime.utcnow(),
                "bestseller": True
            },
            {
                "_id": "aaaae",
                "name": "Women Round Neck Cotton Top",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 130,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Women",
                "subCategory": "Topwear",
                "sizes": ["M", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaaf",
                "name": "Girls Round Neck Cotton Top",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 140,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Kids",
                "subCategory": "Topwear",
                "sizes": ["S", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaag",
                "name": "Men Tapered Fit Flat-Front Trousers",
                "description": "A garment worn from the waist to the ankles, covering both legs separately (rather than with cloth extending across both legs as in a skirt or dress).",
                "price": 190,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Men",
                "subCategory": "Bottomwear",
                "sizes": ["S", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaah",
                "name": "Men Round Neck Pure Cotton T-shirt",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 140,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Men",
                "subCategory": "Topwear",
                "sizes": ["S", "M", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaai",
                "name": "Girls Round Neck Cotton Top",
                "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
                "price": 100,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Kids",
                "subCategory": "Topwear",
                "sizes": ["M", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            },
            {
                "_id": "aaaaj",
                "name": "Men Tapered Fit Flat-Front Trousers",
                "description": "A garment worn from the waist to the ankles, covering both legs separately (rather than with cloth extending across both legs as in a skirt or dress).",
                "price": 110,
                "image": ["https://www.sporto.in/cdn/shop/files/SP-TEE637-WHT_other2.jpg?v=1714719670"],
                "category": "Men",
                "subCategory": "Bottomwear",
                "sizes": ["S", "L", "XL"],
                "date": datetime.utcnow(),
                "bestseller": False
            }
        ]
        
        # Insert products
        result = db.products.insert_many(products_data)
        print(f"✅ Inserted {len(result.inserted_ids)} products")
        
        # Create a test user with hashed password
        test_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password_hash": generate_password_hash("test123"),
            "cart": [],
            "created_at": datetime.utcnow()
        }
        
        user_result = db.users.insert_one(test_user)
        print(f"✅ Created test user with ID: {user_result.inserted_id}")
        print("   Email: test@example.com")
        print("   Password: test123")
        
        print("\n🎉 Database seeded successfully!")
        
        # Verify the data
        product_count = db.products.count_documents({})
        user_count = db.users.count_documents({})
        
        print(f"\n📊 Database Summary:")
        print(f"   Total products: {product_count}")
        print(f"   Total users: {user_count}")
        
        # Show some sample products
        print("\n📦 Sample products:")
        for product in db.products.find().limit(3):
            print(f"   - {product['name']} (ID: {product['_id']}, Price: ${product['price']})")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    seed_database()
