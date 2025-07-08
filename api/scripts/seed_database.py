# seed_database.py
import os
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
load_dotenv()

def seed_database():
    # 1) Connect to MongoDB
    MONGODB_URI = os.environ.get('MONGODB_URI')
    client = MongoClient(MONGODB_URI)
    db = client["ecom"]
    print("🌱 Starting database seeding...")

    # 2) Clear existing collections
    db.products.delete_many({})
    db.carts.delete_many({})
    db.orders.delete_many({})
    print("🧹 Collections cleared!")

    # 3) Base URL for "image"s served by your React app
    IMG_BASE = "http://localhost:3000/src/assets/"

    # 4) Sample products data
    # CORRECTION: Fixed multiple syntax errors, incorrect booleans, and inconsistent data.
    products_data = [
        {
            "_id": "aaaaa",
            "name": "Women Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 100,
            "image": ['https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQGgXEUuw3nsNThA4t8mlrHfsCPlasjdPxK46Fe5TFMSOskMt9iMYPlJwdfj7KmmJ_BeiCPKN8wGRL9yjYdYsUsT1ozI4pVB6f30bVrZTDs'],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L"],
            "date": 1716634345448,
            "bestseller": True
        },
        {
            "_id": "aaaab",
            "name": "Men Round Neck Pure Cotton T‑shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves.",
            "price": 200,
            "image": [
                IMG_BASE + "p_img2_1.png",
                IMG_BASE + "p_img2_2.png",
                IMG_BASE + "p_img2_3.png",
                IMG_BASE + "p_img2_4.png"
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
            "description": "A lightweight, usually knitted, pullover shirt with a round neckline and short sleeves.",
            "price": 220,
            "image": [IMG_BASE + "p_img3.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "L", "XL"],
            "date": 1716234545448,
            "bestseller": True
        },
        {
            "_id": "aaaad",
            "name": "Men Round Neck Pure Cotton T‑shirt",
            "description": "A comfortable pullover shirt with a close fit and a round neckline.",
            "price": 110,
            "image": [IMG_BASE + "p_img4.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "XXL"],
            "date": 1716621345448,
            "bestseller": True
        },
        {
            "_id": "aaaae",
            "name": "Women Round Neck Cotton Top",
            "description": "A lightweight cotton top with a round neckline and short sleeves.",
            "price": 130,
            "image": [IMG_BASE + "p_img5.png"],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["M", "L", "XL"],
            "date": 1716622345448,
            "bestseller": True
        },
        {
            "_id": "aaaaf",
            "name": "Girls Round Neck Cotton Top",
            "description": "A knitted pullover shirt with a round neckline, perfect for kids.",
            "price": 140,
            "image": [IMG_BASE + "p_img6.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "L", "XL"],
            "date": 1716623423448,
            "bestseller": True
        },
        {
            "_id": "aaaag",
            "name": "Men Tapered Fit Flat‑Front Trousers",
            "description": "Classic flat-front trousers with a modern tapered leg.",
            "price": 190,
            "image": [IMG_BASE + "p_img7.png"],
            "category": "Men",
            "subCategory": "Bottomwear",
            "sizes": ["S", "L", "XL"],
            "date": 1716621542448,
            "bestseller": False
        },
        {
            "_id": "aaaah",
            "name": "Men Round Neck Pure Cotton T‑shirt",
            "description": "Breathable pure cotton tee with a round neck.",
            "price": 140,
            "image": [IMG_BASE + "p_img8.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716622345448,
            "bestseller": False
        },
        {
            "_id": "aaaai",
            "name": "Girls Round Neck Cotton Top",
            "description": "Comfortable cotton top for girls with short sleeves.",
            "price": 100,
            "image": [IMG_BASE + "p_img9.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["M", "L", "XL"],
            "date": 1716621235448,
            "bestseller": False
        },
        {
            "_id": "aaaaj",
            "name": "Men Tapered Fit Flat‑Front Trousers",
            "description": "Lightweight trousers with a flattering tapered fit.",
            "price": 110,
            "image": [IMG_BASE + "p_img10.png"],
            "category": "Men",
            "subCategory": "Bottomwear",
            "sizes": ["S", "L", "XL"],
            "date": 1716622235448,
            "bestseller": False
        },
        {
            "_id": "aaaak",
            "name": "Men Round Neck Pure Cotton T‑shirt",
            "description": "Soft pure cotton tee with round neck design.",
            "price": 120,
            "image": [IMG_BASE + "p_img11.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L"],
            "date": 1716623345448,
            "bestseller": False
        },
        {
            "_id": "aaaal",
            "name": "Men Round Neck Pure Cotton T‑shirt",
            "description": "Classic pure cotton tee for everyday wear.",
            "price": 150,
            "image": [IMG_BASE + "p_img12.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716624445448,
            "bestseller": False
        },
        {
            "_id": "aaaam",
            "name": "Women Round Neck Cotton Top",
            "description": "Casual cotton top with a comfortable fit.",
            "price": 130,
            "image": [IMG_BASE + "p_img13.png"],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716625545448,
            "bestseller": False
        },
        {
            "_id": "aaaan",
            "name": "Boy Round Neck Pure Cotton T‑shirt",
            "description": "Pure cotton tee designed for boys with a round neckline.",
            "price": 160,
            "image": [IMG_BASE + "p_img14.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716626645448,
            "bestseller": False
        },
        {
            "_id": "aaaao",
            "name": "Men Tapered Fit Flat‑Front Trousers",
            "description": "Modern tapered trousers with a flat front design.",
            "price": 140,
            "image": [IMG_BASE + "p_img15.png"],
            "category": "Men",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716627745448,
            "bestseller": False
        },
        {
            "_id": "aaaap",
            "name": "Girls Round Neck Cotton Top",
            "description": "Everyday casual cotton top for girls.",
            "price": 170,
            "image": [IMG_BASE + "p_img16.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716628845448,
            "bestseller": False
        },
        {
            "_id": "aaaaq",
            "name": "Men Tapered Fit Flat-Front Trousers",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 150,
            "image": [IMG_BASE + "p_img17.png"],
            "category": "Men",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716629945448,
            "bestseller": False
        },
        {
            "_id": "aaaar",
            "name": "Boy Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 180,
            "image": [IMG_BASE + "p_img18.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716631045448,
            "bestseller": False
        },
        {
            "_id": "aaaas",
            "name": "Boy Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 160,
            "image": [IMG_BASE + "p_img19.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716632145448,
            "bestseller": False
        },
        {
            "_id": "aaaat",
            "name": "Women Palazzo Pants with Waist Belt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 190,
            "image": [IMG_BASE + "p_img20.png"],
            "category": "Women",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716633245448,
            "bestseller": False
        },
        {
            "_id": "aaaau",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 170,
            "image": [IMG_BASE + "p_img21.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716634345448,
            "bestseller": False
        },
        {
            "_id": "aaaav",
            "name": "Women Palazzo Pants with Waist Belt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 200,
            "image": [IMG_BASE + "p_img22.png"],
            "category": "Women",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716635445448,
            "bestseller": False
        },
        {
            "_id": "aaaaw",
            "name": "Boy Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 180,
            "image": [IMG_BASE + "p_img23.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716636545448,
            "bestseller": False
        },
        # CORRECTION: Separated two merged objects and added the missing image key.
        {
            "_id": "aaaax",
            "name": "Boy Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 210,
            "image": [IMG_BASE + "p_img24.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716637645448,
            "bestseller": False
        },
        {
            "_id": "aaaay",
            "name": "Girls Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 190,
            "image": [IMG_BASE + "p_img25.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716638745448,
            "bestseller": False
        },
        {
            "_id": "aaaaz",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 220,
            "image": [IMG_BASE + "p_img26.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716639845448,
            "bestseller": False
        },
        # CORRECTION: Removed an extra empty dictionary object {} here.
        {
            "_id": "aaaba",
            "name": "Girls Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 200,
            "image": [IMG_BASE + "p_img27.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716640945448,
            "bestseller": False
        },
        {
            "_id": "aaabb",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 230,
            "image": [IMG_BASE + "p_img28.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716642045448,
            "bestseller": False
        },
        {
            "_id": "aaabc",
            "name": "Women Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 210,
            "image": [IMG_BASE + "p_img29.png"],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716643145448,
            "bestseller": False
        },
        {
            "_id": "aaabd",
            "name": "Girls Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 240,
            "image": [IMG_BASE + "p_img30.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716644245448,
            "bestseller": False
        },
        {
            "_id": "aaabe",
            "name": "Men Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 220,
            "image": [IMG_BASE + "p_img31.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716645345448,
            "bestseller": False
        },
        {
            "_id": "aaabf",
            "name": "Men Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 250,
            "image": [IMG_BASE + "p_img32.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716646445448,
            "bestseller": False
        },
        {
            "_id": "aaabg",
            "name": "Girls Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 230,
            "image": [IMG_BASE + "p_img33.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716647545448,
            "bestseller": False
        },
        {
            "_id": "aaabh",
            "name": "Women Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 260,
            "image": [IMG_BASE + "p_img34.png"],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716648645448,
            "bestseller": False
        },
        {
            "_id": "aaabi",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 240,
            "image": [IMG_BASE + "p_img35.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716649745448,
            "bestseller": False
        },
        {
            "_id": "aaabj",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 270,
            "image": [IMG_BASE + "p_img36.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716650845448,
            "bestseller": False
        },
        {
            "_id": "aaabk",
            "name": "Women Round Neck Cotton Top",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 250,
            "image": [IMG_BASE + "p_img37.png"],
            "category": "Women",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716651945448,
            "bestseller": False
        },
        {
            "_id": "aaabl",
            "name": "Men Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 280,
            "image": [IMG_BASE + "p_img38.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716653045448,
            "bestseller": False
        },
        {
            "_id": "aaabm",
            "name": "Men Printed Plain Cotton Shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 260,
            "image": [IMG_BASE + "p_img39.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716654145448,
            "bestseller": False
        },
        {
            "_id": "aaabn",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 290,
            "image": [IMG_BASE + "p_img40.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716655245448,
            "bestseller": False
        },
        {
            "_id": "aaabo",
            "name": "Men Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 270,
            "image": [IMG_BASE + "p_img41.png"],
            "category": "Men",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716656345448,
            "bestseller": False
        },
        {
            "_id": "aaabp",
            "name": "Boy Round Neck Pure Cotton T-shirt",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 300,
            "image": [IMG_BASE + "p_img42.png"],
            "category": "Kids",
            "subCategory": "Topwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716657445448,
            "bestseller": False
        },
        {
            "_id": "aaabq",
            "name": "Kid Tapered Slim Fit Trouser",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 280,
            "image": [IMG_BASE + "p_img43.png"],
            "category": "Kids",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716658545448,
            "bestseller": False
        },
        {
            "_id": "aaabr",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 310,
            "image": [IMG_BASE + "p_img44.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716659645448,
            "bestseller": False
        },
        {
            "_id": "aaabs",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 290,
            "image": [IMG_BASE + "p_img45.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716660745448,
            "bestseller": False
        },
        {
            "_id": "aaabt",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 320,
            "image": [IMG_BASE + "p_img46.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716661845448,
            "bestseller": False
        },
        {
            "_id": "aaabu",
            "name": "Kid Tapered Slim Fit Trouser",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 300,
            "image": [IMG_BASE + "p_img47.png"],
            "category": "Kids",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716662945448,
            "bestseller": False
        },
        # CORRECTION: Separated two merged objects and added the missing image key.
        {
            "_id": "aaabv",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 330,
            "image": [IMG_BASE + "p_img48.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716664045448,
            "bestseller": False
        },
        {
            "_id": "aaabw",
            "name": "Kid Tapered Slim Fit Trouser",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 310,
            "image": [IMG_BASE + "p_img49.png"],
            "category": "Kids",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716665145448,
            "bestseller": False
        },
        {
            "_id": "aaabx",
            "name": "Kid Tapered Slim Fit Trouser",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 300,
            "image": [IMG_BASE + "p_img50.png"],
            "category": "Kids",
            "subCategory": "Bottomwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716666245448,
            "bestseller": False
        },
        # CORRECTION: Removed an extra empty dictionary object {} here.
        {
            "_id": "aaaby",
            "name": "Women Zip-Front Relaxed Fit Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 320,
            "image": [IMG_BASE + "p_img51.png"],
            "category": "Women",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716667345448,
            "bestseller": False
        },
        {
            "_id": "aaabz",
            "name": "Men Slim Fit Relaxed Denim Jacket",
            "description": "A lightweight, usually knitted, pullover shirt, close-fitting and with a round neckline and short sleeves, worn as an undershirt or outer garment.",
            "price": 350,
            "image": [IMG_BASE + "p_img52.png"],
            "category": "Men",
            "subCategory": "Winterwear",
            "sizes": ["S", "M", "L", "XL"],
            "date": 1716668445448,
            "bestseller": False
        }
    ]

    # 5) Insert products
    if products_data:
        result = db.products.insert_many(products_data)
        print(f"✅ Inserted {len(result.inserted_ids)} products")

    # 6) Create a test user
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": generate_password_hash("test123"), # Renamed to 'password' for clarity
        "cart": [],
        "created_at": datetime.utcnow()
    }
    # Use update_one with upsert=True to avoid creating duplicate users on re-runs
    db.users.update_one(
        {"email": test_user["email"]},
        {"$set": test_user},
        upsert=True
    )
    print(f"✅ Upserted test user")
    print("   Email: test@example.com")
    print("   Password: test123")

    # 7) Summary
    product_count = db.products.count_documents({})
    user_count = db.users.count_documents({})
    print("\n🎉 Database seeded successfully!")
    print(f"📊 Total products: {product_count}")
    print(f"📊 Total users:    {user_count}")

    client.close()

if __name__ == "__main__":
    seed_database()