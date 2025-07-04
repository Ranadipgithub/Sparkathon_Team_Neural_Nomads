import os
import sys
import subprocess
import time
import requests

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✓ MongoDB is running")
        return True
    except Exception as e:
        print(f"✗ MongoDB is not running: {e}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = ['flask', 'flask-cors', 'flask-jwt-extended', 'pymongo', 'werkzeug']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is not installed")
    
    if missing_packages:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def start_flask_app():
    """Start the Flask application"""
    print("\nStarting Flask backend...")
    
    # Change to api directory
    api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api')
    os.chdir(api_dir)
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Start Flask app
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\nFlask backend stopped.")
    except Exception as e:
        print(f"Error starting Flask app: {e}")

def main():
    print("E-commerce Backend Startup Script")
    print("=" * 40)
    
    # Check MongoDB
    if not check_mongodb():
        print("\nPlease start MongoDB first:")
        print("- On Windows: net start MongoDB")
        print("- On macOS: brew services start mongodb-community")
        print("- On Linux: sudo systemctl start mongod")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Start Flask app
    start_flask_app()

if __name__ == '__main__':
    main()
