import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
import json
from datetime import datetime

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/ecommerce')

# Sample products data (matching your frontend assets)
products_data = [
    {
        "_id": "aaaaa",
        "name": "Women Round Neck Cotton Top",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 100,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img1.png"],
        "category": "Women",
        "subCategory": "Topwear",
        "sizes": ["S", "M", "L"],
        "date": 1716634345448,
        "bestseller": True
    },
    {
        "_id": "aaaab",
        "name": "Men Round Neck Pure Cotton T-shirt",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 200,
        "image": [
            "/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img2_1.png",
            "/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img2_2.png",
            "/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img2_3.png",
            "/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img2_4.png"
        ],
        "category": "Men",
        "subCategory": "Topwear",
        "sizes": ["M", "L", "XL"],
        "date": 1716621345448,
        "bestseller": True
    },
    {
        "_id": "aaaac",
        "name": "Girls Round Neck Cotton Top",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 220,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img3.png"],
        "category": "Kids",
        "subCategory": "Topwear",
        "sizes": ["S", "L", "XL"],
        "date": 1716234545448,
        "bestseller": True
    },
    {
        "_id": "aaaad",
        "name": "Men Round Neck Pure Cotton T-shirt",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 110,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img4.png"],
        "category": "Men",
        "subCategory": "Topwear",
        "sizes": ["S", "M", "XXL"],
        "date": 1716621345448,
        "bestseller": True
    },
    {
        "_id": "aaaae",
        "name": "Women Round Neck Cotton Top",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 130,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img5.png"],
        "category": "Women",
        "subCategory": "Topwear",
        "sizes": ["M", "L", "XL"],
        "date": 1716622345448,
        "bestseller": True
    },
    {
        "_id": "aaaaf",
        "name": "Girls Round Neck Cotton Top",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 140,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img6.png"],
        "category": "Kids",
        "subCategory": "Topwear",
        "sizes": ["S", "L", "XL"],
        "date": 1716623423448,
        "bestseller": True
    },
    {
        "_id": "aaaag",
        "name": "Men Tapered Fit Flat-Front Trousers",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 190,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img7.png"],
        "category": "Men",
        "subCategory": "Bottomwear",
        "sizes": ["S", "L", "XL"],
        "date": 1716621542448,
        "bestseller": False
    },
    {
        "_id": "aaaah",
        "name": "Men Round Neck Pure Cotton T-shirt",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 140,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img8.png"],
        "category": "Men",
        "subCategory": "Topwear",
        "sizes": ["S", "M", "L", "XL"],
        "date": 1716622345448,
        "bestseller": False
    },
    {
        "_id": "aaaai",
        "name": "Girls Round Neck Cotton Top",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 100,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img9.png"],
        "category": "Kids",
        "subCategory": "Topwear",
        "sizes": ["M", "L", "XL"],
        "date": 1716621235448,
        "bestseller": False
    },
    {
        "_id": "aaaaj",
        "name": "Men Tapered Fit Flat-Front Trousers",
        "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
        "price": 110,
        "image": ["/Sparkathon_Team_Neural_Nomads/frontend/src/assets/p_img10.png"],
        "category": "Men",
        "subCategory": "Bottomwear",
        "sizes": ["S", "L", "XL"],
        "date": 1716622235448,
        "bestseller": False
    }
]

def seed_database():
    try:
        # Connect to MongoDB with explicit database name
        client = MongoClient(MONGODB_URI)
        
        # Extract database name from URI or use default
        if 'mongodb+srv://' in MONGODB_URI or 'mongodb://' in MONGODB_URI:
            # Parse database name from URI
            if '/' in MONGODB_URI.split('?')[0]:
                db_name = MONGODB_URI.split('/')[-1].split('?')[0]
            else:
                db_name = 'ecommerce'  # fallback
        else:
            db_name = 'ecommerce'
        
        print(f"Using database: {db_name}")
        db = client[db_name]
        
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        
        # Check if products collection exists and count documents
        existing_count = db.products.count_documents({})
        print(f"Existing products in database: {existing_count}")
        
        # Clear existing products
        if existing_count > 0:
            delete_result = db.products.delete_many({})
            print(f"Deleted {delete_result.deleted_count} existing products")
        
        # Insert sample products
        print(f"Inserting {len(products_data)} products...")
        result = db.products.insert_many(products_data)
        print(f"Successfully inserted {len(result.inserted_ids)} products!")
        
        # Verify insertion
        final_count = db.products.count_documents({})
        print(f"Final product count in database: {final_count}")
        
        # Show sample of inserted data
        sample_product = db.products.find_one()
        if sample_product:
            print(f"Sample product: {sample_product['name']} (ID: {sample_product['_id']})")
        
        # Create indexes for better performance
        try:
            db.products.create_index("category")
            db.products.create_index("subCategory")
            db.products.create_index("bestseller")
            db.products.create_index([("name", "text")])  # Text search index
            print("Created database indexes")
        except Exception as idx_error:
            print(f"Warning: Could not create some indexes: {idx_error}")
        
        # Create indexes for other collections
        try:
            db.users.create_index("email", unique=True)
            db.cart_items.create_index([("user_id", 1), ("product_id", 1), ("size", 1)])
            db.orders.create_index("user_id")
            print("Created additional indexes")
        except Exception as idx_error:
            print(f"Warning: Could not create some indexes: {idx_error}")
        
        client.close()
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        print(f"MongoDB URI: {MONGODB_URI}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    seed_database()
