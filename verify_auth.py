import requests
import time

BASE_URL = "http://localhost:8000"

def test_auth():
    email = f"test_{int(time.time())}@example.com"
    password = "testpassword123"

    print(f"Testing with email: {email}")

    # 1. Signup
    print("Testing Signup...")
    signup_data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    print(f"Signup Response: {response.status_code} - {response.json()}")
    
    if response.status_code != 200:
        print("Signup failed!")
        return

    # 2. Login
    print("\nTesting Login...")
    login_data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login Response: {response.status_code} - {response.json()}")

    if response.status_code == 200:
        print("\nAuth test passed!")
    else:
        print("\nAuth test failed!")

if __name__ == "__main__":
    # Note: This script assumes the server is running at localhost:8000
    # You can start it with: uvicorn main:app --reload
    try:
        test_auth()
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Please ensure uvicorn is running.")
