import requests
import json

# API base URL
BASE_URL = 'http://127.0.0.1:5328'

def test_api():
    print("Testing E-commerce API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 2: Root endpoint
    print("2. Testing root endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 3: API info
    print("3. Testing API info...")
    try:
        response = requests.get(f'{BASE_URL}/api')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 4: Get products
    print("4. Testing get products...")
    try:
        response = requests.get(f'{BASE_URL}/api/products/')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Product count: {data.get('count', 0)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 5: Get latest products
    print("5. Testing get latest products...")
    try:
        response = requests.get(f'{BASE_URL}/api/products/latest?limit=5')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Product count: {data.get('count', 0)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 6: Get bestsellers
    print("6. Testing get bestsellers...")
    try:
        response = requests.get(f'{BASE_URL}/api/products/bestsellers?limit=5')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Product count: {data.get('count', 0)}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 7: Register user
    print("7. Testing user registration...")
    try:
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=user_data)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        
        # Store token for further tests
        global access_token
        access_token = data.get('access_token')
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    print("API testing completed!")

if __name__ == '__main__':
    test_api()
